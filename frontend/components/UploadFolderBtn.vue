<script setup lang="ts">
import { FolderPlusIcon } from "@heroicons/vue/24/solid";

async function onUpload() {
  const filePaths = await chooseFiles("folder", ["py"]);
  console.log(filePaths);
}
</script>

<template>
    <Button severity="info" class="font-bold" @click="onUpload">Upload Folder<FolderPlusIcon class="w-6 h-6 ml-1"/></Button>
</template>
