<script setup lang="ts">
import { resolveResource } from "@tauri-apps/api/path";
import { convertFileSrc } from "@tauri-apps/api/tauri";
import { ALL_LYLA_STATES } from "@/composables/lylaState";
import type { AnimationAction } from "three";

const { scene: canvasScene } = useTresContext();
const lylaStateStore = useLylaStateStore();

// model (no animations)
const modelPath = await resolveResource(`resources/models/lyla.glb`);
const modelAssetUrl = convertFileSrc(modelPath);
const { scene: model, nodes } = await useGLTF(modelAssetUrl, { draco: true });

// background
const backgroundPath = await resolveResource(
  `resources/textures/background.jpeg`
);
const backgroundAssetUrl = convertFileSrc(backgroundPath);
const backgroundTexture = await useTexture([backgroundAssetUrl]);
canvasScene.value.background = backgroundTexture;

// model (animations)
onMounted(async () => {
  // init all actions
  const actions: { [actionName: string]: AnimationAction } = {};
  for (const state of ALL_LYLA_STATES) {
    const { action, name } = await createAction(
      `resources/animations/Lyla${state}.fbx`,
      model,
      state
    );
    actions[name] = action;
  }

  actions[lylaStateStore.$state.name].play();

  // subscribe to changes in state
  lylaStateStore.$subscribe((_, state) => {
    actions[state.name].play();
  });
});
</script>

<template>
  <primitive :object="model" :scale="2" :position="[0, -3, 5]" />
  <TresAmbientLight :intensity="2.5" />
</template>
