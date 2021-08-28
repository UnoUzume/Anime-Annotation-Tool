<template>
  <div
    class="cv-collapse-item el-collapse-item"
    :class="{ 'is-active': isActive, 'is-disabled': disabled }"
  >
    <div
      :id="`el-collapse-head-${id}`"
      class="el-collapse-item__header"
      :tabindex="disabled ? -1 : 0"
      :class="{
        focusing: focusing,
        'is-active': isActive,
      }"
      @click="handleHeaderClick"
      @keyup.space.enter.stop="handleEnterClick"
      @focus="handleFocus"
      @blur="focusing = false"
    >
      <el-checkbox
        v-model="checked"
        @change="doThis"
        @click.stop=""
      ></el-checkbox>
      <slot name="header"></slot>
      <i
        class="el-collapse-item__arrow el-icon-arrow-right"
        :class="{ 'is-active': isActive }"
      >
      </i>
    </div>
    <el-collapse-transition>
      <div
        v-show="isActive"
        :id="`el-collapse-content-${id}`"
        class="el-collapse-item__wrap"
      >
        <div class="el-collapse-item__content">
          <slot></slot>
        </div>
      </div>
    </el-collapse-transition>
  </div>
</template>
<script lang='ts'>
import { defineComponent, PropType, inject, computed, ref } from 'vue'
import { CollapseProvider } from './CvCollapse.vue'

const generateId = (): number => Math.floor(Math.random() * 10000)
// import ElCollapseTransition from '@element-plus/components/collapse-transition'

export default defineComponent({
  // name: 'ElCollapseItem',
  props: {
    title: {
      type: String,
      default: '',
    },
    name: {
      type: [String, Number] as PropType<string | number>,
      default: () => {
        return generateId()
      },
    },
    disabled: Boolean,
    func: String,
  },
  setup(props) {
    const collapse = inject<CollapseProvider>('collapse')
    const collapseMitt = collapse?.collapseMitt

    const contentWrapStyle = ref({
      height: 'auto',
      display: 'block',
    })
    const contentHeight = ref(0)
    const focusing = ref(false)
    const isClick = ref(false)
    const checked = ref(false)
    const id = ref(generateId())

    const isActive = computed(() => {
      return collapse?.activeNames.value.indexOf(props.name) > -1
    })

    const handleFocus = () => {
      setTimeout(() => {
        if (!isClick.value) {
          focusing.value = true
        } else {
          isClick.value = false
        }
      }, 50)
    }

    const handleHeaderClick = () => {
      if (props.disabled) return
      collapseMitt?.emit('item-click', props.name)
      focusing.value = false
      isClick.value = true
    }

    const handleEnterClick = () => {
      collapseMitt?.emit('item-click', props.name)
    }
    const doThis = (val) => {
      console.log('doThis!' + val)
    }

    return {
      isActive,
      contentWrapStyle,
      contentHeight,
      focusing,
      isClick,
      id,
      handleFocus,
      handleHeaderClick,
      handleEnterClick,
      collapse,
      doThis,
      checked,
    }
  },
})
</script>
