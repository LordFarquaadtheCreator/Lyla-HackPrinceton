import { appWindow, PhysicalSize } from '@tauri-apps/api/window';

const MIN_WIDTH = 1770;
const MIN_HEIGHT = 978;

export default async function() {
    await appWindow.setMinSize(new PhysicalSize(MIN_WIDTH, MIN_HEIGHT));
}