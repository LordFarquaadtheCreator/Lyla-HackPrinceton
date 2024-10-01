import { resolveResource } from "@tauri-apps/api/path";
import { convertFileSrc } from "@tauri-apps/api/tauri";
import type { Scene } from "three";

/**
 * Create action from mixamo.com animation.
 * 
 * @param fbxPath 
 * @param target 
 */
export default async function<T extends string>(fbxPath: string, target: Scene, name: T) {
    const animPath = await resolveResource(fbxPath);
    const animAssetUrl = convertFileSrc(animPath);
    const { animations } = await useFBX(animAssetUrl);
    const { actions } = useAnimations(animations, target);
    
    return {
        name,
        action: actions["mixamo.com"]
    };
}