<template>
  <cv-collapse v-model="activeNames" @change="handleChange">
    <component
      v-for="item in modelValue"
      :key="item.name"
      :is="'cv-func-' + item.func"
      :name="item.name"
      v-model:argForm="item.argForm"
    ></component>
  </cv-collapse>
</template>

<script>
import CvCollapse from './CvCollapse.vue'
import CvFuncPaint from './CvFuncPaint.vue'
import CvFuncCut from './CvFuncCut.vue'
export default {
  data() {
    return {
      activeNames: [],
      change: 'two',
    }
  },
  emits: ['update:modelValue'],
  props: {
    func: String,
    name: String,
    modelValue: Array,
  },
  components: { CvCollapse, CvFuncPaint, CvFuncCut },
  methods: {
    handleChange(value) {
      console.log(value)
    },
  },
  computed: {
    getFullComName() {
      return 'cv-func-' + this.func
    },
  },
}
</script>

<style scoped>
a {
  color: #42b983;
}
</style>
