<template>
    <div id="app">
        <p>
           - TIMER -
        </p>
        <br>
        <p>
            {{isTimerRunning ? "実行中" : "停止中"}}
        </p>
        <p class="time">
            {{leftTime}}
        </p>

        <button @click="startTimer">start</button>
        <button @click="stopTimer">stop</button>
    </div>
</template>

<script lang="ts">
    import {Component, Vue} from 'vue-property-decorator';
    import {TimerClient} from "./timer_grpc_web_pb";
    import {Empty, StartRequest, TimerState} from "./timer_pb";
    import {ClientReadableStream} from "grpc-web";

    @Component({})
    export default class App extends Vue {
        private timerClient: TimerClient;
        private isTimerRunning: boolean = false;
        private leftTime: number = 0;

        constructor() {
            super();
            this.timerClient = new TimerClient('http://' + window.location.hostname + ':8081', null, null);
        }

        private startTimer(): void {
            const request = new StartRequest();
            request.setTime(10);  // 10秒をセット
            const stream: ClientReadableStream<TimerState> = this.timerClient.startTimer(request, {});
            stream.on('data', (response: TimerState) => {
                this.isTimerRunning = response.getIsrunning();
                this.leftTime = response.getLefttime();
            });
        }

        private stopTimer(): void {
            this.timerClient.stopTimer(new Empty(), {}, (err, response: TimerState) => {
                this.isTimerRunning = response.getIsrunning();
                this.leftTime = response.getLefttime();
            });
        }

    }
</script>

<style lang="scss">
    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        margin-top: 60px;
    }
    .time{
        margin:0 0 40px 0;
        font-size:148px;
        color:#999;
    }
</style>
