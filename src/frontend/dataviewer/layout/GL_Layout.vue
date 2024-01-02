
<template>
    <div style="position: relative">
        <div ref="root" style="position: absolute; width: 100%; height: 100%">
            <!-- Root DOM for golden-layout manager -->
        </div>
        <div style="position: absolute; width: 100%; height: 100%">
            <GL_Component
                v-for="[ind, view] in ViewComponents"
                :key="ind"
                :ref="(el) => GLFunctionRef(el, ind)"
            >
                <component :is="view"/>
            </GL_Component>
        </div>
    </div>
</template>


<script setup lang="ts">

import { 
    defineAsyncComponent, 
    onMounted, 
    ref, 
    markRaw, 
    nextTick, 
    getCurrentInstance,
    Ref,
    ComponentPublicInstance
} from 'vue';
import {
    ComponentContainer, 
    Json,
    LayoutConfig, 
    RowOrColumnItemConfig, 
    StackItemConfig,
    ComponentItemConfig, 
    ResolvedComponentItemConfig, 
    LogicalZIndex, 
    VirtualLayout,
    ResolvedLayoutConfig
} from 'golden-layout';
import GL_Component from "@/frontend/dataviewer/layout/GL_Component.vue";
import Test from "@/frontend/dataviewer/views/Test.vue"


/***********************************
/*  State   
/***********************************/
const root = ref<HTMLElement | null>(null);
let layout: VirtualLayout;

const GLComponents = new Map<
    ComponentContainer, 
    {refId: number, component: InstanceType<typeof GL_Component>}
>(); 
const GLRefs = ref(new Map<number, InstanceType<typeof GL_Component>>());
const ViewComponents = ref(new Map<number, any>());  

let curIndex = 0;
let GLBoundingClientRect: DOMRect;
const instance = getCurrentInstance();


/***********************************
/*  Methods   
/***********************************/
/* @internal */
const GLFunctionRef = (ref: ComponentPublicInstance | null | Element, ind: number) => {
    GLRefs.value.set(ind, ref as InstanceType<typeof GL_Component>)
}

/* @internal */
function addComponent(componentType: string): number {
    const view = markRaw(
        defineAsyncComponent(
            () => import('../views/Test.vue')
        )
    );
    let index = curIndex;
    curIndex++;

    ViewComponents.value.set(index, view);
    return index;
}

async function addGLComponent(componentType: string, title: string): Promise<void> {
    if (componentType.length == 0)
        throw new Error("addGLComponent: component's type is empty");

    const index = addComponent(componentType);      // add component to list of Views
    await nextTick();  
    layout.addComponent(componentType, {refId: index}, title);      // register component with golden-layout
}

/***********************************
/*  Mount 
/***********************************/
onMounted(() => {
    if (root.value == null) throw new Error("GoldenLayout can't find the root DOM!");

    function onResize(): void {
        const dom = root.value;
        const width  = dom ? dom.offsetWidth : 0;
        const height = dom ? dom.offsetHeight : 0;

        layout.setSize(width, height);
    }
    window.addEventListener("resize", onResize, { passive: true });

    /***********************************
    /*  GoldenLayout Event Handlers     
    /***********************************/
    function handleBeforeVirtualRecting(count: number): void {
        GLBoundingClientRect = (root.value as HTMLElement).getBoundingClientRect();
    }
    function handleContainerVirtualRecting(container: ComponentContainer, width: number, height: number): void {
        // Fetch component from GLC map
        const componentObj = GLComponents.get(container);
        if (!componentObj || !componentObj?.component) {
            throw new Error("handleContainerVirtualRecting: Component not found");
        }

        // calculate component's relative position
        const containerBoundingClientRect = container.element.getBoundingClientRect();
        const left = containerBoundingClientRect.left - GLBoundingClientRect.left;
        const top = containerBoundingClientRect.top - GLBoundingClientRect.top;

        // update position
        componentObj.component.setPosAndSize(left, top, width, height);
    }


    function handleContainerVisibility(container: ComponentContainer, visible: boolean): void {
        // Fetch component from GLC map
        const componentObj = GLComponents.get(container);
        if (!componentObj || !componentObj?.component) {
            throw new Error("handleContainerVisibility: Component not found");
        }

        // set visibility
        componentObj.component.setVisibility(visible);
    }


    function handleContainerZIndex(container: ComponentContainer, logicalZIndex: LogicalZIndex, defaultZIndex: string): void {
        // Fetch component from GLC map
        const componentObj = GLComponents.get(container);
        if (!componentObj || !componentObj?.component) {
            throw new Error("handleContainerZIndex: Component not found");
        }

        // set ZIndex
        componentObj.component.setZIndex(defaultZIndex);
    }


    function handleBindComponent(
        container: ComponentContainer, 
        itemConfig: ResolvedComponentItemConfig
    ): ComponentContainer.BindableComponent {
        // Fetch GL component and store it in the map
        let refId = -1;
        if (itemConfig && itemConfig.componentState) {
            refId = (itemConfig.componentState as Json).refId as number;
        } else {
            throw new Error(
                "bindComponentEventListener: component has no ref id"
            )
        }
        const component = GLRefs.value.get(refId);
        GLComponents.set(container, {refId: refId, component: component})

        // add event handlers to container
        container.virtualRectingRequiredEvent = (container, width, height) => 
            handleContainerVirtualRecting(container, width, height)
        
        container.virtualVisibilityChangeRequiredEvent = (container, visible) => 
            handleContainerVisibility(container, visible)
        
        container.virtualZIndexChangeRequiredEvent = (container, logicalZIndex, defaultZIndex) => 
            handleContainerZIndex(container, logicalZIndex, defaultZIndex)
        
        // return BindableComponent
        return {
            component,
            virtual: true
        }
    }


    function handleUnbindComponent(container: ComponentContainer): void {
        // Fetch component from GLC map
        const componentObj = GLComponents.get(container);
        if (!componentObj || !componentObj?.component) {
            throw new Error("handleUnbindComponentEvent: Component not found");
        }

        // Remove container from GLC and corresponding view from View map
        GLComponents.delete(container);
        ViewComponents.value.delete(componentObj.refId);
        GLRefs.value.delete(componentObj.refId);
    }


    // Instantiate layout
    layout = new VirtualLayout(
        root.value as HTMLElement,
        handleBindComponent,
        handleUnbindComponent
    );
    layout.beforeVirtualRectingEvent = handleBeforeVirtualRecting;
})

defineExpose({
    addGLComponent,
});

</script>
