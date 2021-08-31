<template>
  <div class="workspace__canvas-wrapper" ref="canvasWrapper">
    <div
      class="workspace__canvas-box"
      ref="canvasBox"
      :style="{ transform: `scale(${this.boxScale})` }"
      @mousedown="whenMouseDown($event)"
      @mousewheel="whenMouseWheel($event)"
    >
      <img class="workspace__frame" src="/static/canvas.png" alt="" />
      <canvas
        class="workspace__color-water"
        width="960"
        height="540"
        ref="colorWater"
        :style="{ opacity: this.annTool.colorWaterAlpha }"
        v-show="this.annTool.isShowColorWater"
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
        :style="{ opacity: this.annTool.colorCanvasAlpha }"
        v-show="this.annTool.isShowColorCanvas"
      ></canvas>
    </div>
    <div class="workspace__cursor" :style="cusorStyle" ref="cursor">
      <svg xmlns="http://www.w3.org/2000/svg" version="1.1">
        <rect
          :width="annTool.brushSize"
          :height="annTool.brushSize"
          :style="{ fill: '#' + this.active_label.bgc }"
        ></rect>
      </svg>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      maskCanvas_ctx: null,
      colorCanvas_ctx: null,
      colorWater_ctx: null,
      boxHeight: 0,
      boxScale: 1,
      cursorSize: 20,
      isEmpty: false,
      isDrawMoving: false,
      isCanvasMoving: false,
      canvasXc: 0,
      canvasYc: 0,
    }
  },
  computed: {
    cusorScale() {
      return this.boxHeight / 540
    },
    cusorStyle() {
      return {
        transform: `translate(-50%, -50%) scale(${this.cusorScale})`,
        width: this.annTool.brushSize + 'px',
        height: this.annTool.brushSize + 'px',
      }
    },
  },
  inject: ['annTool', 'active_label'],
  created() {
    this.$nextTick(() => {
      // this.cursor = this.$refs.cursor
      this.maskCanvas_ctx = this.$refs.maskCanvas.getContext('2d')
      this.colorCanvas_ctx = this.$refs.colorCanvas.getContext('2d')
      this.colorWater_ctx = this.$refs.colorWater.getContext('2d')
      this.canvasPushdo()

      document.body.addEventListener('mousemove', this.cursorMove)
      document.addEventListener('mousemove', this.drawMoving)
      document.addEventListener('mousemove', this.canvasMoving)
      document.addEventListener('mouseup', this.whenMouseUp)
      this.boxHeight = this.$refs.canvasBox.getBoundingClientRect().height
    })
    this.$store.watch(
      (state, getters) => getters.getMCan,
      (value) => {
        this.maskCanvas_ctx.putImageData(value, 0, 0)
      }
    )
    this.$store.watch(
      (state, getters) => getters.getCCan,
      (value) => {
        this.colorCanvas_ctx.putImageData(value, 0, 0)
      }
    )
  },
  mounted() {
    window.canvasClear = this.canvasClear
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
      if (e.button == 0 && this.isdrawMoving) {
        this.isdrawMoving = false
        this.canvasPushdo()
      } else if (e.button == 1) this.isCanvasMoving = false
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
        this.isEmpty = false
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
    whenMouseWheel(e) {
      let wheel = e.wheelDelta > 0 ? 1 : -1
      let dscale = wheel * 0.1
      if (e.shiftKey) {
        let newScale = this.boxScale + dscale
        if (newScale >= 0.5) {
          this.annTool.brushSize *= this.boxScale / newScale
          this.boxScale += dscale
        }
        //原文链接：https://blog.csdn.net/qq_36281882/article/details/107056406
      } else {
        this.annTool.brushSize += wheel
        if (this.annTool.brushSize < 1) {
          this.annTool.brushSize = 1
        } else if (this.annTool.brushSize > 50) {
          this.annTool.brushSize = 50
        }
      }
    },
    canvasClear() {
      this.colorCanvas_ctx.clearRect(0, 0, 960, 540)
      this.maskCanvas_ctx.clearRect(0, 0, 960, 540)
      this.isEmpty = true
      this.canvasPushdo()
    },
    canvasResize() {
      this.annTool.brushSize *= this.boxScale
      this.boxScale = 1
      this.$refs.canvasBox.style.left = '0px'
      this.$refs.canvasBox.style.top = '0px'
    },
    canvasUndo() {
      this.$store.commit('canvasUndo')
    },
    canvasRedo() {
      this.$store.commit('canvasRedo')
    },
    canvasPushdo() {
      this.$store.commit(
        'canvasPushdo',
        this.colorCanvas_ctx.getImageData(0, 0, 960, 540),
        this.maskCanvas_ctx.getImageData(0, 0, 960, 540)
      )
    },
  },
  watch: {
    boxScale() {
      this.$nextTick(() => {
        this.boxHeight = this.$refs.canvasBox.getBoundingClientRect().height
      })
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
}
.workspace__cursor {
  position: absolute;
  left: 0px;
  top: 0px;
  transform: translate(-50%, -50%);
  pointer-events: none;
  opacity: 0.7;
}
</style>
