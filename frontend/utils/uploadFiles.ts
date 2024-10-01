import { Body, fetch } from "@tauri-apps/api/http";

const UPLOAD_FILES_API_ENDPOINT = "";

export default async function (filePaths: string[]) {
  await fetch(UPLOAD_FILES_API_ENDPOINT, {
    method: "POST",
    timeout: 30,
    body: Body.json(filePaths)
  });
}
