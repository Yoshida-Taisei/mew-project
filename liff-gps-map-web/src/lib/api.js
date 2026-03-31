export function parseLambdaBody(payload) {
  if (!payload) return null;
  const body = payload.body;
  if (body == null) return payload;
  if (typeof body === "string") {
    try {
      return JSON.parse(body);
    } catch {
      return body;
    }
  }
  return body;
}

