# Vue.js Essentials

Source: Vue.js
Chapter: 1
Created time: December 3, 2023 12:30 PM
Date: December 5, 2023 12:04 AM

- An application instance won’t render until its `.mount()` method is called, Vue will automatically use the container’s `innerHTML` as the template if the root component doesn’t have a `template`
- The application instance exposes a `.config` object that allows us to configure app-level options like error handling. These must be applied before mounting the app

### Template Syntax

- **Text Interpolation:** `<span>Message: {{ msg }}</span>`  — the mustache tag (double curly braces) will be replaced with the value of the `msg` property from the component instance, and updated whenever `msg` changes.
- **Raw HTML:** using the `v-html` directive renders plain HTML from a string, ignoring data bindings.
- **Attribute Bindings:** Mustaches can’t be used inside HTML attributes, instead we have to use a `v-bind` directive — `<div v-bind:id="dynamicId"></div>` to keep the element’s attribute in sync with the component’s property. A very common shorthand for `v-bind:`  is just `:`
- **Using JavaScript Expressions:** Vue supports the use of full JavaScript expressions inside text interpolations and the attribute values of any Vue directives
    - **************************************************Template expressions are sandboxed and only have access to a restricted list of globals. To included other globals, you have to add them to************************************************** `app.config.globalProperties`
- **Dynamic Arguments:** We can also use JavaScript in a directive argument by wrapping it with square brackets — `<a v-bind:[attributeName]="url"> ... </a>`
    - Dynamic argument expressions are expected to evaluate to a string or `null`.
- **Modifiers:** Modifiers are special fields denoted by a dot that indicate that a directive should be constrained in a certain way.

### Reactivity Fundamentals

- **Declaring Reactive State:** The recommended way to declare reactive state is using the `ref()` function:
    
    ```jsx
    import { ref } from "vue";
    
    const count = ref(0);
    ```
    
    `ref()` returns an object with the argument  as the object’s `.value` property. 
    
- We need refs because Vue’s reactivity system needs to detect changes to variables and update the DOM accordingly. There’s no way to do this in standard JavaScript, so wrapping an object in a ref can be thought of as including custom getters and setters that can track changes and trigger updates. This also lets you pass refs into functions while still having access to the latest value (think `String` and `Integer` in Java)
- **Deep Reactivity:** Refs can hold any value type including nested objects, and applying ref to a value also makes all the nested components reactive. For performance reasons, it might be desirable to opt-out of this deep reactivity behavior, which can be done with shallow refs. **This is especially useful for very large objects.**
- `reactive()` is another way to declare reactive state, but it is recommended to use `ref()` as the primary API for reactivity due to limitations of `reactive()`.

### Computed Properties

- For complex logic that includes reactive data, it is recommended to use a ******computed property******. Here’s an example:
    
    ```jsx
    <script setup>
    import { reactive, computed } from 'vue'
    
    const author = reactive({
      name: 'John Doe',
      books: [
        'Vue 2 - Advanced Guide',
        'Vue 3 - Basic Guide',
        'Vue 4 - The Mystery'
      ]
    })
    
    // a computed ref
    const publishedBooksMessage = computed(() => {
      return author.books.length > 0 ? 'Yes' : 'No'
    })
    </script>
    
    <template>
      <p>Has published books:</p>
      <span>{{ publishedBooksMessage }}</span>
    </template>
    ```
    
    We’ve declared a computed property `publishedBooksMessage` by using the `computed()` function, which expects a getter function and returns a computed ref. Computed properties automatically track their reactive dependencies and are recomputed whenever a dependency changes. This is faster than simply using a method because computed properties **********cache********** their values — if the property is accessed and no dependencies have changed since the last access, it immediately returns the cached value instead of calling the getter again. This provides a noticeable speedup when the computation is particularly expensive.
    
- Getters should be side-effect free (i.e. don’t call async functions or mutate the DOM) and we preferably shouldn’t mutate computed values (instead mutate the dependencies)

### Class and Style Bindings

- **Binding HTML Classes:** We can pass an object to `:class` to dynamically toggles classes — `<div :class="{ active: isActive }"></div>` — the `active` class will be included if `isActive` is truthy. We can also bind to a list of classes, or to computed properties that return an object.
    - ********************************With Components:******************************** When used on a component with a single root, the bound classes are merged with any classes already on the root element. If the component has multiple root elements, you must define which element will receive the class using the `$attrs` component property :
        
        ```jsx
        <!-- MyComponent template using $attrs -->
        <p :class="$attrs.class">Hi!</p>
        <span>This is a child component</span>
        ```
        
- **************Binding Inline Styles:************** `:style` supports binding to JavaScript object values — `<div :style="{ color: activeColor, fontSize: fontSize + 'px' }"></div>` . `:style` supports both camelCase and kebab-cased CSS properties, and usually `:style` is bound to a (computed) style object to make the template cleaner.

### Conditional Rendering

- **`v-if` :** `v-if` is used to conditionally render a block, the block will be rendered if the directive’s expression is truthy — `<h1 v-if="awesome">Vue is awesome!</h1>`
- **`v-else` :** `v-else` is used to indicate an else block for `v-if` —
    
    ```jsx
    <button @click="awesome = !awesome">Toggle</button>
    
    <h1 v-if="awesome">Vue is awesome!</h1>
    <h1 v-else>Oh no 😢</h1>
    ```
    
    A `v-else` element must immediately follow a `v-if` or `v-else-if` element.
    
- **`v-else-if`:** `v-else` serves as an else if block for `v-if`. It can be chained multiple times and must immediately follow a `v-if` or `v-else-if` element.
- **`v-if` on `<template>`:** `v-if` can only be applied to single elements since it is a directive. If we want to toggle more than one element, we can wrap then in a `<template>` element and use `v-if` on the template.
- `**v-show`:** Similar to `v-if` in functionality, but elements with `v-show` are rendered into the DOM with the CSS property `display: false`, while `v-if` properly destroys and re-creates event listeners and child components inside the conditional block.

### List Rendering

- **`v-for`:** We can use the `v-for` directive to render a list of items based on an array, and we can included an optional second alias for the index of the current item —
    
    ```jsx
    const parentMessage = ref('Parent')
    const items = ref([{ message: 'Foo' }, { message: 'Bar'}])
    
    <li v-for="(item, index) in items">
    	{{ parentMessage }} - {{ index }} - {{ item.message }}
    </li>
    ```
    
- `**v-for` with an Object:** We can also use `v-for` to iterate through the properties of an object, with second and third aliases for the property’s name and index, respectively —
    
    ```jsx
    const myObject = reactive({
      title: 'How to do lists in Vue',
      author: 'Jane Doe',
      publishedAt: '2016-04-10'
    })
    
    <li v-for="(value, key, index) in myObject">
      {{ index }}. {{ key }}: {{ value }}
    </li>
    ```
    
- **`v-for` with a Range/on `<template>`:** `v-for` can also take an integer in place of a list. In this case, it will repeat the template that many times. Like `v-if`, `v-for` can be used on `<template>` elements if we want to render a block of elements.
- ************Maintaining State with `key`:** To make view reuse and reorder existing stateful DOM elements when the order of elements in the underlying list changes, we need to provide a unique `key` attribute for each item —
    
    ```jsx
    <template v-for="todo in todos" :key="todo.name">
      <li>{{ todo.name }}</li>
    </template>
    ```
    
    It is recommended to use `key` whenever possible.
    
- **`v-for` with a Component:** We can directly use `v-for` on a component, but we need to use props to explicitly pass the data into the component —
    
    ```jsx
    <MyComponent
      v-for="(item, index) in items"
      :item="item"
      :index="index"
      :key="item.id"
    />
    ```
    
- ******************************************Array Change Detection:****************************************** Vue can detect when a reactive array’s mutation methods are called and trigger necessary updates. If we use non-mutating methods like `filter` and `concat`, we need to make sure to replace the old array with the new one. If we want to display a filtered or sorted version of an array without actually mutating the original data, we can create a computed property (or a function if computed properties are not feasible) that returns the filtered or sorted array.

### Event Handling

- ********************************Listening to Events:******************************** We can use the `v-on` directive (shorthand `@`) to listen to DOM events and run JavaScript when they’re triggered by adding `@click="handler"` to the element’s attributes. The handler value can either be inline JavaScript or a method handler that points to a method defined on the component.
- **************Calling Methods in Inline Handlers:************** We can also call methods in an inline handler, which lets us pass the method custom arguments instead of the native event. If we need access to the original DOM event in an inline handler, we can pass it to a method using the `$event` variable or use an inline arrow function.
- ********************************Event and Key Modifiers:******************************** To avoid calling event modifiers inside event handlers, Vue provides ****************************event modifiers**************************** for `v-on` that can be chained to the event handler given to `@`. Vue also lets us check for key modifiers when listening for key events, which lets us check for specific keys. It provides key aliases for commonly used keys, system modifier keys, and mouse buttons. It also provides the `.exact` modifier so we can detect the exact combination of system modifiers need to trigger an event.

### Form Input Bindings

- When dealing with forms, we need to sync the state of form input elements with the corresponding JavaScript state. To avoid manually wiring up event value bindings and changing event listeners, the `v-model` directive can simplify input bindings to `<input v-model="text>`.
- If we want to change the the string/boolean values that correspond to input state for the radio, checkbox, and select options, we can bind them to static values using the `value` attribute or to dynamic properties using the `:value` `v-bind` binding.
- There are also modifiers for update frequency and input formatting — `.lazy` syncs the input with data after `change` events instead of after `input` events, `.number` automatically typecasts the input as a number, and `.trim` automatically trims whitespace from the input.

### Lifecycle Hooks

- Each Vue component instance goes through a series of initialization steps when it’s created. It also exposes ******************************lifecycle hooks****************************** along the way, which allow us the opportunity to add our own code at specific stages. For example, the `onMounted` hook can be used to run code after the component has finished the initial rendering and created the DOM nodes. There are also other hooks which will be called at different stages of the instance’s lifecycle with the most commonly used being `onMounted`, `onUpdated`, and `onUnmounted` —
    
    ```jsx
    <script setup>
    import { onMounted } from 'vue'
    
    onMounted(() => {
      console.log(`the component is now mounted.`)
    })
    </script>
    ```
    
    Hooks must be registered ****************synchronously**************** during component setup.
    

### Watchers

- **`watch`:** Computed properties let us declaratively compute derived values, but if we want to perform “side effects” in response to state changes, we need to use the `watch` function —
    
    ```jsx
    <script setup>
    import { ref, watch } from 'vue'
    
    const question = ref('')
    const answer = ref('Questions usually contain a question mark. ;-)')
    const loading = ref(false)
    
    // watch works directly on a ref
    watch(question, async (newQuestion, oldQuestion) => {
      if (newQuestion.includes('?')) {
        loading.value = true
        answer.value = 'Thinking...'
        try {
          const res = await fetch('https://yesno.wtf/api')
          answer.value = (await res.json()).answer
        } catch (error) {
          answer.value = 'Error! Could not reach the API. ' + error
        } finally {
          loading.value = false
        }
      }
    })
    </script>
    
    <template>
      <p>
        Ask a yes/no question:
        <input v-model="question" :disabled="loading" />
      </p>
      <p>{{ answer }}</p>
    </template>
    ```
    
    `watch`'s first argument can be any reactive source — a ref, a computed ref, a reactive object, a getter function, or an array of sources.
    
- ****************************Deep Watchers:**************************** If you call `watch()` directly on a reactive object, it automatically creates a deep watcher (the callback is triggered on mutations of any of the nested elements). This can get very expensive for large data structures, so we should usually give `watch` a getter that returns a reactive object — this creates a shallow watcher.
- ******************************Eager Watchers:****************************** By default, `watch` doesn’t call the callback until the value has been changed. If we instead want the callback to be triggered once on creation, we can pass the `{ immediate: true }` option.
- **`watchEffect()`:** `watchEffect()` combines dependency tracking and side effects into one phase — it automatically tracks any reactive property accessed in its function body. This removes the burden of having to maintain the list of dependencies manually, and can provide performance gains for large data structures, since `wacthEffect()` only tracks the elements that are used in the callback.
- ********************************************Callback Flush Timing:******************************************** When a reactive state is mutated, it can trigger both Vue component updates and user-defined updates; user-defined updates are triggered first by default, which means that DOM accesses during the user-defined update will be to a stale DOM. If we want a watcher callback to access the DOM after Vue updates, we can pass in the `{ flush: post }` option or use the `watchPostEffect()` function.
- **************************************Stopping a Watcher:************************************** Usually, watchers are created synchronously with a component and will automatically be stopped when the component is unmounted. However, watchers created in an async callback are not bound to the component and must be stopped manually to avoid memory leaks. This is done using the returned handle function —
    
    ```jsx
    const unwatch = watchEffect(() => {})
    
    // ...later, when no longer needed
    unwatch()
    ```
    

### Template Refs

- ******************Accessing the Refs:****************** There may be some cases when we need access to a DOM element. To do this, we declare a ref an bind it to a DOM element with the `ref` attribute —
    
    ```jsx
    <script setup>
    import { ref, onMounted } from 'vue'
    
    // declare a ref to hold the element reference
    // the name must match template ref value
    const input = ref(null)
    
    onMounted(() => {
      input.value.focus()
    })
    </script>
    
    <template>
      <input ref="input" />
    </template>
    ```
    
- **************************************Refs inside `v-for`:** When `ref` is used inside `v-for`, the ref should contain an Array value, which will be populated with the DOM elements as they are mounted.
- ****************************Function refs:**************************** If we want to use a function to decide where element references are stored instead, we can use the dynamic `:ref` binding and pass it an inline function or method instead of a static ref name string.
- **************************************Ref on a Component:************************************** `ref` can also be used to create a reference to a child component, but the parent won’t be able to access properties of the child that are not exposed using the `defineExpose()` macro. **Instead, we should try to implement parent/child interactions using the standard props and emit interfaces first.**

### Components Basics

-