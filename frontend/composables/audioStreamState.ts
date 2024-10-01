import { defineStore } from "pinia";

interface AudioStreamState {
    stream: MediaStream | null;
    recorder: MediaRecorder | null;
    chunks: Blob[];
}
interface AudioStreamMethods {
    startRecording: () => Promise<void>;
    stopRecording: () => Promise<void>;
}

export const useAudioStreamStateStore = defineStore<"audioStreamState", AudioStreamState, {}, AudioStreamMethods>("audioStreamState", {
  state: () => {
    return { stream: null, recorder: null, chunks: [] };
  },
  actions: {
    async startRecording() {
        this.$state.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        this.$state.recorder = new MediaRecorder(this.$state.stream);

        this.$state.recorder.ondataavailable = e => {
            this.$state.chunks.push(e.data);
        };
        this.$state.recorder.onstop = async e => {
            const mp4 = this.$state.chunks.reduce((a, b)=> new Blob([a, b], {type: "audio/mp4"}));
            const mp4Buffer = await mp4.arrayBuffer();

            this.$state.chunks = []
        };
        this.$state.recorder.start();
    },
    async stopRecording() {
        this.$state.recorder?.stop();
        this.$state.stream?.getTracks().forEach(track => track.stop());
        this.$state.recorder = null;
        this.$state.stream = null;
    }
  },
});
