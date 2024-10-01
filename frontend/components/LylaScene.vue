<script setup lang="ts"></script>

<template>
  <div>
    <TresCanvas alpha shadows>
      <TresPerspectiveCamera :position="[0, 0, 8]" :fov="42" />
      <Suspense>
        <LylaModel />
        <template #fallback>Loading...</template>
      </Suspense>
    </TresCanvas>
  </div>
</template>
