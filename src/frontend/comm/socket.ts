import { ref } from "vue";
import { io, Socket} from "socket.io-client";
import { Payload, StringPayload } from "@/frontend/comm/payloadTypes"

export function useWebSocket() {
    const socket = ref<Socket | null>(null);

    function connectSocket(url: string): void {
        if (socket.value){
            disconnectSocket();
        }
        socket.value = io(url);
        socket.value.on('connect', () => console.log('connected from client!'))
    }
    
    function disconnectSocket(): void {
        if (socket.value) {
            socket.value.disconnect();
        }
    }

    function emitSocketEvent<P extends Payload>(ev: string, payload: P): void {
        if (socket.value)
            socket.value.emit(ev, payload)
        else
            throw new Error("emitSocketEvent: socket hasn't been initialized")
    }

    function addSocketListener(ev: string, listener: (...args: any[]) => void): void {
        if (socket.value)
            socket.value.on(ev, listener)
        else
            throw new Error("addSocketListener: socket hasn't been initialized")
    }

    return {
        connectSocket,
        disconnectSocket, 
        emitSocketEvent,
        addSocketListener
    };

}