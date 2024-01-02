<template>
    <div class="full-height">
        <div id="nav" style="height: 90px">
            <button @click="onClickAddComponent">Add Component</button>
        </div>
    <GL_Layout 
        ref="layout"
        style="width: 100%; height: calc(90% - 90px)"
    />
    </div>
</template>

<script setup lang='ts'>
import GL_Layout from './layout/GL_Layout.vue'
import { ref} from 'vue'

const layout = ref<InstanceType<typeof GL_Layout> | null>(null);  // this stores a reference to the layout DOM element
console.log('👋 This message is being logged by "App.vue", included via Vite');

const onClickAddComponent = () => {
    layout.value?.addGLComponent("Test", "Test")
    console.log("button pressed")
}
</script>

<style>
html {
    height: 100%;
}
body {
    height: 100%;
    border: 10px;
    margin: 0;
    overflow: hidden;
}
.full-height, #app {
    height: 100%;
    width: 100%;
}
#app {
    font-family: Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}
#nav {
    text-align: center;
}
</style>

<style src="golden-layout/dist/css/goldenlayout-base.css"></style>
<style src="golden-layout/dist/css/themes/goldenlayout-dark-theme.css"></style>

