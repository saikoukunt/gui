<template>
    <!-- style="position: absolute; overflow: hidden" -->
    <div ref="ViewDiv" style="position: absolute; overflow: hidden;">
        <slot></slot>
    </div>

</template>

<script setup lang="ts">
import { ref } from 'vue';

const ViewDiv = ref<null | HTMLElement>(null);

/* @internal */
function numberToPixels(value: number): string {
    return value.toString(10) + "px";
}

function setPosAndSize(left: number, top: number, width: number, height: number): void {
    if (ViewDiv.value) {
        const el = ViewDiv.value as HTMLElement;
        el.style.left = numberToPixels(left);
        el.style.top = numberToPixels(top);
        el.style.width = numberToPixels(width);
        el.style.height = numberToPixels(height);
    }
}


function setVisibility(visible: boolean): void {
    if (ViewDiv.value) {
        const el = ViewDiv.value as HTMLElement;
        if (visible) {
            el.style.display = "";
        } else {
            el.style.display = "none";
        }
    }
}


function setZIndex(zIndex: string) {
    if (ViewDiv.value) {
        const el = ViewDiv.value as HTMLElement;
        el.style.zIndex = zIndex;
    }
}

defineExpose({
    setPosAndSize,
    setVisibility,
    setZIndex
});
</script>