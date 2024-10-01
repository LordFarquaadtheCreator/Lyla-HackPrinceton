<script setup lang="ts">
const recentPath = useRecentPathStore();
</script>

<template>
  <div class="flex flex-col items-center justify-center gap-3">
    <UploadFileBtn class="w-1/2" />
    <UploadFolderBtn class="w-1/2" />
    <UploadLeetcodeBtn class="w-1/2" />
    <div class="h-1/16" />
    <div class="text-center">
      Current Path: <span class="italic">{{ recentPath.$state.path }}</span>
    </div>
  </div>
</template>
