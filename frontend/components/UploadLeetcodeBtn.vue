<script setup lang="ts">
import { CodeBracketIcon } from "@heroicons/vue/24/solid";

async function onUpload() {
}
</script>

<template>
    <Button severity="warning" class="font-bold" @click="onUpload">Upload LeetCode<CodeBracketIcon class="w-6 h-6 ml-1"/></Button>
</template>