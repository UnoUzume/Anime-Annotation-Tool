<template>
  <cv-collapse-item :name="name">
    <template v-slot:header>
      <div>Paint</div>
    </template>
    <div>CvFuncPaint {{ randomNumber }}</div>
  </cv-collapse-item>
</template>

<script>
import axios from 'axios'
import CvCollapseItem from './CvCollapseItem.vue'
export default {
  data() {
    return {
      randomNumber: 0,
    }
  },
  props: {
    name: String,
  },
  components: {
    CvCollapseItem,
  },
  methods: {
    getRandom() {
      // this.randomNumber = this.getRandomInt(1, 100)
      this.randomNumber = this.getRandomFromBackend()
    },

    getRandomFromBackend() {
      const path = `http://localhost:5000/api/`
      axios
        .get(path)
        .then((response) => {
          this.randomNumber = response.data
        })
        .catch((error) => {
          console.log(error)
        })
    },
  },
  created() {
    this.getRandom()
  },
}
</script>

<style scoped>
</style>
