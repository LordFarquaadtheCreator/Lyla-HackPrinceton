import { Store } from "tauri-plugin-store-api";

const store = new Store(".settings.dat");

export default async function (path: string) {
    const recentPathStore = useRecentPathStore();
    await store.set("recent-path", { value: path });
    await recentPathStore.updateRecentPath();
}
