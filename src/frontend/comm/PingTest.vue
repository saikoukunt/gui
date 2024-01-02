<template>
    <button @click="connectBackend">connect to backend</button>
    <button @click="pingTest">send ping</button>
</template>

<script setup lang="ts">
import { useWebSocket } from "@/frontend/comm/socket";
import { StringPayload } from "@/frontend/comm/payloadTypes";
import { io, Socket} from "socket.io-client";

const {connectSocket, emitSocketEvent, addSocketListener } = useWebSocket();

let socket : Socket;

function connectBackend() : void {
    connectSocket("http://localhost:3000/");
    addSocketListener(
        'backend-msg', 
        (msg: string) => {console.log(msg)}
    );
    // socket = io("http://localhost:3000/");
}

function pingTest(): void {
    emitSocketEvent<StringPayload>("frontend-msg", {str: "hewwo uwu"})
}

</script>