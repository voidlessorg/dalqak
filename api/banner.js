export const config = { api: { bodyParser: false } };

const URL_ = process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL;
const TOKEN_ = process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN;

async function redis(cmd) {
  const r = await fetch(URL_, {
    method: "POST",
    headers: { Authorization: "Bearer " + TOKEN_ },
    body: JSON.stringify(cmd),
  });
  return (await r.json()).result;
}

async function readBody(req) {
  const chunks = [];
  for await (const c of req) chunks.push(c);
  return Buffer.concat(chunks);
}

export default async function handler(req, res) {
  const q = req.query || {};

  if ("version" in q) return res.status(200).send("v2");

  if (req.method === "POST") {
    if (q.token !== process.env.BANNER_TOKEN) return res.status(403).send("forbidden");
    const buf = await readBody(req);
    if (buf.length < 100 || buf.length > 700000) return res.status(413).send("bad size");
    const b64 = buf.toString("base64");
    if (q.ip) await redis(["SET", "ip:" + q.ip, b64, "EX", 1800]);
    else await redis(["SET", "banner", b64]);
    return res.status(200).send("ok");
  }

  const ip = (req.headers["x-forwarded-for"] || "").split(",")[0].trim()
          || req.headers["x-real-ip"] || "";
  let b64 = ip ? await redis(["GET", "ip:" + ip]) : null;
  if (!b64) b64 = await redis(["GET", "banner"]);
  if (!b64) return res.status(404).send("no banner yet");

  const img = Buffer.from(b64, "base64");
  res.setHeader("Content-Type", img[0] === 0xff ? "image/jpeg" : "image/png");
  res.setHeader("Cache-Control", "no-store");
  res.status(200).send(img);
}
