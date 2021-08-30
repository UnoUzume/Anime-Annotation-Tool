<template>
  <div class="workspace__canvas-wrapper" ref="canvasWrapper">
    <div
      class="workspace__canvas-box"
      ref="canvasBox"
      @mousedown="whenMouseDown($event)"
      @mousewheel="whenMouseWheel($event)"
    >
      <img class="workspace__frame" src="/static/canvas.png" alt="" />
      <canvas
        class="workspace__color-water"
        width="960"
        height="540"
        ref="colorWater"
      ></canvas>
      <canvas
        class="workspace__mask-canvas"
        width="960"
        height="540"
        ref="maskCanvas"
      ></canvas>
      <canvas
        class="workspace__color-canvas"
        width="960"
        height="540"
        ref="colorCanvas"
      ></canvas>
    </div>
    <div class="workspace__cursor" ref="cursor" :style="cusorStyle">
      <svg xmlns="http://www.w3.org/2000/svg" version="1.1">
        <rect width="20" height="20"></rect>
      </svg>
    </div>
  </div>
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
      maskCanvas_ctx: null,
      colorCanvas_ctx: null,
      colorWater_ctx: null,
      colorCanvasHeight: 0,
      isDrawMoving: false,
      isCanvasMoving: false,
      canvasXc: 0,
      canvasYc: 0,
    }
  },
  // inject: {
  //   annTool: {
  //     default: () => {},
  //   },
  // },
  inject: ['annTool', 'active_label'],
  emits: ['update:modelValue'],
  props: {
    func: String,
    name: String,
    modelValue: Array,
  },
  components: { CvCollapse, CvFuncPaint, CvFuncCut },
  created() {
    this.$nextTick(() => {
      // this.cursor = this.$refs.cursor
      this.maskCanvas_ctx = this.$refs.maskCanvas.getContext('2d')
      this.colorCanvas_ctx = this.$refs.colorCanvas.getContext('2d')
      this.colorWater_ctx = this.$refs.colorWater.getContext('2d')
      document.body.addEventListener('mousemove', this.cursorMove)

      document.addEventListener('mousemove', this.drawMoving)
      document.addEventListener('mousemove', this.canvasMoving)
      document.addEventListener('mouseup', this.whenMouseUp)

      this.colorCanvasHeight =
        this.$refs.colorCanvas.getBoundingClientRect().height
    })
  },
  methods: {
    cursorMove(e) {
      let r = this.$refs.canvasWrapper.getBoundingClientRect()
      this.$refs.cursor.style.left = e.clientX - r.left + 'px'
      this.$refs.cursor.style.top = e.clientY - r.top + 'px'
    },
    whenMouseDown(e) {
      if (e.button == 0) {
        this.isdrawMoving = true
        this.drawMoving(e)
      } else if (e.button == 1) {
        if (e.preventDefault) e.preventDefault()
        this.canvasXc = e.pageX - this.$refs.canvasBox.offsetLeft
        this.canvasYc = e.pageY - this.$refs.canvasBox.offsetTop
        this.isCanvasMoving = true
      }
    },
    whenMouseUp(e) {
      if (e.button == 0) this.isdrawMoving = false
      else if (e.button == 1) this.isCanvasMoving = false
    },
    drawMoving(e) {
      if (!this.isdrawMoving) return
      let r = this.$refs.colorCanvas.getBoundingClientRect()
      let fullSize = this.annTool.brushSize
      let halfSize = this.annTool.brushSize / 2
      let x = parseInt(((e.clientX - r.left) / r.width) * 960 - halfSize)
      let y = parseInt(((e.clientY - r.top) / r.height) * 540 - halfSize)
      if (!e.shiftKey) {
        this.colorCanvas_ctx.fillStyle = '#' + this.active_label.bgc
        this.colorCanvas_ctx.fillRect(x, y, fullSize, fullSize)
        // let fill_hex = parseInt(
        //   $('.ann-label__item.active .ann-label__id').val()
        // ).toString(16)
        // if (fill_hex.halfSize == 1) {
        //   fill_hex = '0' + fill_hex
        // }
        // this.maskCanvas_ctx.fillStyle = '#' + fill_hex + fill_hex + fill_hex
        // this.maskCanvas_ctx.fillRect(x, y, halfSize * 2, halfSize * 2)
        this.$refs.colorCanvas.dataset.isEmpty = false
      } else {
        let doubleSize = this.annTool.brushSize * 2
        x = x - halfSize
        y = y - halfSize
        this.colorCanvas_ctx.clearRect(x, y, doubleSize, doubleSize)
        this.maskCanvas_ctx.clearRect(x, y, doubleSize, doubleSize)
      }
    },
    canvasMoving(e) {
      if (!this.isCanvasMoving) return
      this.$refs.canvasBox.style.left = e.pageX - this.canvasXc + 'px'
      this.$refs.canvasBox.style.top = e.pageY - this.canvasYc + 'px'
    },
    // whenMouseWheel(e) {
    //   if (e.shiftKey) {
    //     let scale = parseFloat(
    //       (
    //         $('.workspace__canvas-box')[0].style.transform || `scale(1)`
    //       ).replace(/[^0-9.]/gi, '')
    //     )
    //     let size = e.deltaY * 0.1
    //     if (scale + size >= 0.5) {
    //       $('.workspace__canvas-box')[0].style.transform = `scale(${
    //         scale + size
    //       })`
    //       $('.ann-tool__brush-size').val(
    //         (parseFloat($('.ann-tool__brush-size').val()) * scale) /
    //           (scale + size)
    //       )
    //     }
    //     //原文链接：https://blog.csdn.net/qq_36281882/article/details/107056406
    //     // cursorMove(e);
    //   } else {
    //     let scale = parseFloat(
    //       (
    //         $('.workspace__cursor')[0].style.transform ||
    //         `translate(-50%, -50%) scale(1)`
    //       )
    //         .match(/scale\([0-9.]+\)/)[0]
    //         .replace(/[^0-9.]/gi, '')
    //     )
    //     let size = e.deltaY * 0.1
    //     $(
    //       '.workspace__cursor'
    //     )[0].style.transform = `translate(-50%, -50%) scale(${scale + size})`

    //     $('.ann-tool__brush-size').val(
    //       parseInt($('.ann-tool__brush-size').val()) + e.deltaY
    //     )
    //     if ($('.ann-tool__brush-size').val() < 1) {
    //       $('.ann-tool__brush-size').val(1)
    //     } else if ($('.ann-tool__brush-size').val() > 50) {
    //       $('.ann-tool__brush-size').val(50)
    //     }
    //   }
    // },
  },
  computed: {
    getFullComName() {
      return 'cv-func-' + this.func
    },
    cusorStyle() {
      return {
        transform: `translate(-50%, -50%) scale(${
          this.colorCanvasHeight / 540
        })`,
      }
    },
  },
}
</script>

<style scoped>
.workspace__canvas-wrapper {
  width: calc(100% - 10px);
  height: calc(100% - 10px);
  margin: 5px;
  background-color: rgb(255, 255, 255);
  overflow: hidden;
  position: relative;
}
.workspace__canvas-box {
  height: 100%;
  width: 100%;
  position: relative;
  background-color: white;
  /* overflow: hidden; */
}
.workspace__frame {
  /* max-width: 100%;
    max-height: 100%; */
  height: 100%;
  /* width: 100%; */
}
.workspace__color-water {
  position: absolute;
  left: 0px;
  top: 0px;
  height: 100%;
  opacity: 0.7;
}
.workspace__mask-canvas {
  position: absolute;
  left: 0px;
  top: 0px;
  height: 100%;
  opacity: 0;
}
.workspace__color-canvas {
  position: absolute;
  left: 0px;
  top: 0px;
  /* max-width: 100%;
    max-height: 100%; */
  height: 100%;
  opacity: 0.7;
}
.workspace__cursor {
  position: absolute;
  left: 0px;
  top: 0px;
  width: 20px;
  height: 20px;
  transform: translate(-50%, -50%);
  pointer-events: none;
  opacity: 0.7;
}
</style>
