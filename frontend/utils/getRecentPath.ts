import { Store } from "tauri-plugin-store-api";

const store = new Store(".settings.dat");

export default async function () {
    return (await store.get("recent-path") as any)?.value;
}
