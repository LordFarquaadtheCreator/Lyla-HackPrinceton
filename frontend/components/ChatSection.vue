<script setup lang="ts">
import { resolveResource } from "@tauri-apps/api/path";
import { convertFileSrc } from "@tauri-apps/api/tauri";
import {
  MicrophoneIcon,
  ClockIcon,
  SpeakerWaveIcon,
  SpeakerXMarkIcon,
} from "@heroicons/vue/24/solid";

const audioStreamStateStore = useAudioStreamStateStore();
const toggle = useState(() => false);

async function test() {
  toggle.value = !toggle.value;

  if (toggle.value) {
    return await audioStreamStateStore.startRecording();
  }
  return await audioStreamStateStore.stopRecording();
}

const backgroundPath = await resolveResource(
  `resources/textures/background-blur.jpg`
);
const backgroundAssetUrl = convertFileSrc(backgroundPath);
</script>

<template>
  <div>
    <img :src="backgroundAssetUrl" class="h-full object-cover" />
    <div
      class="absolute top-0 left-0 px-3 pt-4 pb-28 w-full h-full overflow-y-auto"
    >
      <div class="flex flex-col gap-3">
        <LylaMessage />
        <LylaMessage />
      </div>
    </div>
    <div
      class="absolute bottom-0 left-0 w-full bg-gray-400 h-24 z-20 rounded-t-xl"
    >
      <div class="absolute bottom-0 left-0 float-left group">
        <div
          class="flex flex-row gap-1 items-center bg-slate-500 p-2 rounded-t-xl text-white group-hover:bg-slate-300 group-hover:text-black group-hover:cursor-pointer"
        >
          HISTORY
          <ClockIcon class="w-6 h-6 group-hover:animate-spin" />
        </div>
      </div>
      <div class="flex flex-row h-full justify-center items-center gap-5">
        <div class="relative">
          <Button rounded aria-label="Bookmark" severity="info" @click="test">
            <MicrophoneIcon class="h-6 w-6" />
          </Button>
          <div
            class="absolute top-0 left-0 w-full h-full bg-white rounded-full -z-10 animate-ping"
          />
        </div>
      </div>
      <div class="absolute bottom-0 right-0 float-right group">
        <div
          class="flex flex-row gap-1 items-center bg-slate-500 p-2 rounded-t-xl text-white group-hover:bg-slate-300 group-hover:text-black group-hover:cursor-pointer"
        >
          LYLA ON
          <SpeakerWaveIcon class="w-6 h-6" />
        </div>
      </div>
      
    </div>
  </div>
</template>
