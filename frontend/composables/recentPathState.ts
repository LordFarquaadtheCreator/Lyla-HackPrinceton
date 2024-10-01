export const useRecentPathStore = defineStore<"recentPath", { path: string }>(
  "recentPath",
  {
    state: () => {
      return { path: "Select a file/folder." };
    },
    actions: {
      async updateRecentPath() {
        this.$state.path = await getRecentPath() ?? "Select a file/folder.";
      },
    },
  }
);
 