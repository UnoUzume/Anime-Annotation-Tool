<template>
  <div class="e-charts"></div>
</template>

<script>
import axios from 'axios'
import * as echarts from 'echarts'
export default {
  props: ['styles'],
  inject: ['annTool'],
  data() {
    return {
      chart: null,
      diffValue: null,
      options: {
        animation: false,
        tooltip: {
          axisPointer: { type: 'cross', label: { precision: 0 } },
          // position: function (pos, params, dom, rect, size) {
          //   return { top: pos[1], left: pos[0] }
          // },
        },
        grid: { top: 10, bottom: 25, left: 10, right: 15 },
        xAxis: { type: 'category' },
        yAxis: { splitNumber: 3, axisLabel: { show: false } },
        series: [{ name: 'diffValue', type: 'bar', data: [] }],
        visualMap: {
          type: 'piecewise',
          show: false,
          pieces: [{ min: 1e7, color: '#FF9655' }, { max: 1e7 }],
        },
      },
    }
  },
  mounted() {
    this.initChart()
  },
  methods: {
    initChart() {
      // console.log(this.$el)
      this.chart = echarts.init(this.$el)
      this.chart.setOption(this.options)
      // https://blog.csdn.net/smk108/article/details/78482154
      this.chart.getZr().on('click', (params) => {
        const pos = [params.offsetX, params.offsetY]
        if (this.chart.containPixel('grid', pos)) {
          let point = this.chart.convertFromPixel({ seriesIndex: 0 }, pos)
          this.annTool.frameNum =
            point[0] + this.chart.getOption().series[0].data[0][0]
        }
      })
      axios
        .post('/api/get', {
          keys: ['diffValue_cut'],
        })
        .then((res) => {
          let t = res.data.diffValue
          this.diffValue = t.map((value, index) => [index, value])
          this.updateChart(0)
        })
    },
    updateChart(numToGet) {
      if (!this.diffValue) return
      let low = numToGet - 200
      let high = numToGet + 200
      if (low < 0) {
        low = 0
        high = 400
      } else if (high > this.diffValue.length) {
        low = this.diffValue.length - 400
        high = this.diffValue.length
      }
      // console.log(this.diffValue.slice(low, high))
      this.chart.setOption({
        xAxis: { type: 'category' },
        series: [
          {
            name: 'diffValue',
            data: this.diffValue.slice(low, high),
            markLine: {
              symbol: 'none',
              label: { show: false },
              silent: true,
              lineStyle: { color: '#0bd699', width: 3, type: 'solid' },
              data: [{ xAxis: numToGet - low }],
            },
          },
        ],
      })
    },
  },
  watch: {
    'annTool.frameNum': {
      handler(num) {
        this.updateChart(num)
      },
      deep: true,
    },
  },
}
</script>

<style scoped>
.e-charts {
  /* transform: translateY(-52%); */
  max-width: 100%;
  min-width: 100%;
  /* height: 240px; */
  height: 100%;
  /* z-index: -1; */
}
</style>