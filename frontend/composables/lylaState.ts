import { defineStore } from "pinia";

export const ALL_LYLA_STATES = ["Idle", "Thinking", "Talking"] as const;
export type LylaStatesUnion = (typeof ALL_LYLA_STATES)[number];

type LylaDefaultStateInfo = {
  name: LylaStatesUnion;
}
type LylaIdle = LylaDefaultStateInfo & {
  name: "Idle",
};
type LylaThinking = LylaDefaultStateInfo & {
  name: "Thinking",
};
type LylaTalking = LylaDefaultStateInfo & {
  name: "Talking",
};

/**
 * State machine for Lyla model.
 */
export const useLylaStateStore = defineStore<"lylaState", LylaIdle | LylaTalking | LylaThinking>("lylaState", {
  state: () => {
    return { name: "Idle" };
  },
  actions: {
    switchState(state: LylaDefaultStateInfo) {
      this.$state = state;
    },
  },
});
