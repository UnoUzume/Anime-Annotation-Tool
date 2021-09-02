<template>
  <div class="workspace__canvas-wrapper" ref="canWrapper">
    <div
      class="workspace__canvas-box"
      ref="canBox"
      :style="{ transform: `scale(${this.boxScale})` }"
      @mousedown="whenMouseDown($event)"
      @click.right.prevent="whenRightClick($event)"
      @mousewheel="whenMouseWheel($event)"
    >
      <img class="workspace__frame" :src="frameSrc" alt="" />
      <canvas
        id="colorWater"
        class="workspace__canvas"
        width="960"
        height="540"
        ref="cWater"
        :style="{ opacity: this.annTool.cWaterAlpha }"
        v-show="this.annTool.isShowCWater"
      ></canvas>
      <canvas
        id="maskCan"
        class="workspace__canvas"
        width="960"
        height="540"
        ref="mCan"
        style="opacity: 0"
      ></canvas>
      <canvas
        id="colorCan"
        class="workspace__canvas"
        width="960"
        height="540"
        ref="cCan"
        :style="{ opacity: this.annTool.cCanAlpha }"
        v-show="this.annTool.isShowCCan"
      ></canvas>
      <canvas
        id="tempCan1"
        class="workspace__canvas"
        width="960"
        height="540"
        ref="tCan1"
        style="opacity: 1"
      ></canvas>
      <canvas
        id="tempCan2"
        class="workspace__canvas"
        width="960"
        height="540"
        ref="tCan2"
        style="opacity: 1"
      ></canvas>
    </div>
    <div class="workspace__cursor" :style="cusorStyle" ref="cursor">
      <svg xmlns="http://www.w3.org/2000/svg" version="1.1">
        <rect
          :width="annTool.brushSize"
          :height="annTool.brushSize"
          :style="{ fill: '#' + this.activeLabel.bgc }"
        ></rect>
      </svg>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import pako from 'pako'
export default {
  data() {
    return {
      // labelLUT: null,
      frameSrc: '/static/canvas.png',
      mCan_ctx: null,
      cCan_ctx: null,
      tCan1_ctx: null,
      tCan2_ctx: null,
      cWater_ctx: null,
      boxHeight: 0,
      boxScale: 1,
      cursorSize: 20,
      isEmpty: false,
      isDrawMoving: false,
      isCanvasMoving: false,
      isLassoMoving: false,
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
  inject: ['host', 'annTool', 'activeLabel'],
  created() {
    this.$nextTick(() => {
      // this.cursor = this.$refs.cursor
      this.mCan_ctx = this.$refs.mCan.getContext('2d')
      this.cCan_ctx = this.$refs.cCan.getContext('2d')
      this.tCan1_ctx = this.$refs.tCan1.getContext('2d')
      // this.tCan1_ctx.imageSmoothingEnabled = false
      this.tCan2_ctx = this.$refs.tCan2.getContext('2d')
      this.cWater_ctx = this.$refs.cWater.getContext('2d')
      this.canvasPushdo()

      document.body.addEventListener('mousemove', this.cursorMove)
      document.addEventListener('mousemove', this.drawMoving)
      document.addEventListener('mousemove', this.canvasMoving)
      document.addEventListener('mousemove', this.lassoMoving)
      document.addEventListener('mouseup', this.whenMouseUp)
      this.boxHeight = this.$refs.canBox.getBoundingClientRect().height
    })
    this.$store.watch(
      (state, getters) => getters.getUndoMCan,
      (value) =>
        this.mCan_ctx.putImageData(this.$store.getters.toImgData(value), 0, 0)
    )
    this.$store.watch(
      (state, getters) => getters.getUndoCCan,
      (value) =>
        this.cCan_ctx.putImageData(this.$store.getters.toImgData(value), 0, 0)
    )
  },
  mounted() {
    axios.defaults.baseURL = this.host
    // axios.interceptors.request.use((config) => {
    //   config.baseURL = this.host
    //   return config
    // })
    // axios
    //   .post('/api/get', {
    //     keys: ['labelLUT'],
    //   })
    //   .then((res) => {
    //     this.labelLUT = res.data.labelLUT
    //   })
    this.canvasInitsize()
  },
  methods: {
    cursorMove(e) {
      let r = this.$refs.canWrapper.getBoundingClientRect()
      this.$refs.cursor.style.left = e.clientX - r.left + 'px'
      this.$refs.cursor.style.top = e.clientY - r.top + 'px'
    },
    whenMouseDown(e) {
      if (e.button == 0) {
        this.isdrawMoving = true
        this.drawMoving(e)
      } else if (e.button == 1) {
        if (e.preventDefault) e.preventDefault()
        this.canvasXc = e.pageX - this.$refs.canBox.offsetLeft
        this.canvasYc = e.pageY - this.$refs.canBox.offsetTop
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
      let r = this.$refs.cCan.getBoundingClientRect()
      let fullSize = parseInt(this.annTool.brushSize)
      let halfSize = parseInt(fullSize / 2)
      let x = parseInt(((e.clientX - r.left) / r.width) * 960 - halfSize)
      let y = parseInt(((e.clientY - r.top) / r.height) * 540 - halfSize)
      if (!e.shiftKey) {
        this.cCan_ctx.fillStyle = '#' + this.activeLabel.bgc
        this.cCan_ctx.fillRect(x, y, fullSize, fullSize)

        let fill_hex = this.activeLabel.id.toString(16).padStart(2, '0')
        this.mCan_ctx.fillStyle = '#' + fill_hex.repeat(3)
        this.mCan_ctx.fillRect(x, y, fullSize, fullSize)

        this.isEmpty = false
      } else {
        this.cCan_ctx.clearRect(x, y, fullSize, fullSize)
        this.mCan_ctx.clearRect(x, y, fullSize, fullSize)
      }
    },
    canvasMoving(e) {
      if (!this.isCanvasMoving) return
      this.$refs.canBox.style.left = e.pageX - this.canvasXc + 'px'
      this.$refs.canBox.style.top = e.pageY - this.canvasYc + 'px'
    },
    whenRightClick(e) {
      if (!this.isLassoMoving) {
        this.isLassoMoving = true
        this.tCan1_ctx.beginPath()
        let rect = this.$refs.cCan.getBoundingClientRect()
        let x = parseInt(((e.clientX - rect.left) / rect.width) * 960)
        let y = parseInt(((e.clientY - rect.top) / rect.height) * 540)
        this.tCan1_ctx.moveTo(x, y)
      } else {
        this.isLassoMoving = false
        this.tCan1_ctx.fillStyle = '#ffffff'
        this.tCan1_ctx.fill()
        let tCan1_data = this.getImageData(this.tCan1_ctx).data
        let cCan_data = Uint8ClampedArray.from(
          this.getImageData(this.cCan_ctx).data
        )
        let mCan_data = Uint8ClampedArray.from(
          this.getImageData(this.mCan_ctx).data
        )
        let colorR = parseInt(this.activeLabel.bgc.substr(0, 2), 16)
        let colorG = parseInt(this.activeLabel.bgc.substr(2, 2), 16)
        let colorB = parseInt(this.activeLabel.bgc.substr(4, 2), 16)
        for (let index = 0; index < tCan1_data.length; index += 4)
          if (tCan1_data[index + 3] > 250)
            if (!e.shiftKey) {
              cCan_data[index + 0] = colorR
              cCan_data[index + 1] = colorG
              cCan_data[index + 2] = colorB
              cCan_data[index + 3] = 255
              mCan_data[index + 0] = this.activeLabel.id
              mCan_data[index + 1] = this.activeLabel.id
              mCan_data[index + 2] = this.activeLabel.id
              mCan_data[index + 3] = 255
            } else {
              cCan_data[index + 0] = 0
              cCan_data[index + 1] = 0
              cCan_data[index + 2] = 0
              cCan_data[index + 3] = 0
              mCan_data[index + 0] = 0
              mCan_data[index + 1] = 0
              mCan_data[index + 2] = 0
              mCan_data[index + 3] = 0
            }
        if (!e.shiftKey) this.isEmpty = false
        this.cCan_ctx.putImageData(new ImageData(cCan_data, 960, 540), 0, 0)
        this.mCan_ctx.putImageData(new ImageData(mCan_data, 960, 540), 0, 0)
        this.tCan1_ctx.clearRect(0, 0, 960, 540)
        this.tCan2_ctx.clearRect(0, 0, 960, 540)
      }
    },
    lassoMoving(e) {
      if (!this.isLassoMoving) return
      if (e.preventDefault) e.preventDefault()
      let rect = this.$refs.cCan.getBoundingClientRect()
      let x = parseInt(((e.clientX - rect.left) / rect.width) * 960)
      let y = parseInt(((e.clientY - rect.top) / rect.height) * 540)
      this.tCan1_ctx.lineTo(x, y)
      this.tCan2_ctx.beginPath()
      this.tCan2_ctx.lineWidth = '3'
      this.tCan2_ctx.strokeStyle = 'green'
      this.tCan2_ctx.moveTo(x - e.movementX, y - e.movementY)
      this.tCan2_ctx.lineTo(x, y)
      this.tCan2_ctx.stroke()
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
    getImageData(ctx) {
      return ctx.getImageData(0, 0, 960, 540)
    },
    canvasClear() {
      this.cCan_ctx.clearRect(0, 0, 960, 540)
      this.mCan_ctx.clearRect(0, 0, 960, 540)
      this.isEmpty = true
      this.canvasPushdo()
    },
    canvasResize() {
      this.annTool.brushSize *= this.boxScale
      this.boxScale = 1
      this.$refs.canBox.style.left = '0px'
      this.$refs.canBox.style.top = '0px'
    },
    canvasInitsize() {
      let r = this.$refs.canWrapper.getBoundingClientRect()
      // console.log(r)
      if (r.width / r.height < 16 / 9) {
        this.$refs.canBox.style.height = (r.width / r.height / 16) * 900 + '%'
      }
    },
    canvasUndo() {
      this.$store.commit('canvasUndo')
    },
    canvasRedo() {
      this.$store.commit('canvasRedo')
    },
    canvasPushdo() {
      this.$store.commit('canvasPushdo', {
        cCanData: this.getImageData(this.cCan_ctx),
        mCanData: this.getImageData(this.mCan_ctx),
      })
    },
    genWater() {
      if (!this.isEmpty) {
        console.time('genWater time')
        let mCanData = this.getImageData(this.mCan_ctx)
        let mCanData_comped = pako.deflate(mCanData.data, { level: 6 })
        // console.log(mCanData_comped)
        // https://www.cnblogs.com/zhangnan35/p/12433201.html
        let mCanData_b64 = window.btoa(String.fromCharCode(...mCanData_comped))
        // console.timeLog('genWater time')
        axios
          .post('/api/send/gen_water', {
            num_now: this.annTool.frameNum,
            mask_canvas_b64: mCanData_b64,
          })
          .then((res) => {
            // console.timeLog('genWater time')
            // https://www.jianshu.com/p/b48217719c83
            var strData = atob(res.data)
            var charData = strData.split('').map((x) => x.charCodeAt(0))
            var binData = new Uint8Array(charData)
            // console.log(binData)
            let uint8Array = Uint8ClampedArray.from(pako.inflate(binData))
            let cWaterData = new ImageData(uint8Array, 960, 540)
            this.cWater_ctx.putImageData(cWaterData, 0, 0)
            this.annTool.isShowCWater = true
            // console.timeLog('genWater time')
            this.$store.commit('storeCWater', {
              num: this.annTool.frameNum,
              imgData: cWaterData,
            })

            this.$store.commit('storeMCan', {
              num: this.annTool.frameNum,
              imgData: mCanData,
            })
            let cCanData = this.getImageData(this.cCan_ctx)
            this.$store.commit('storeCCan', {
              num: this.annTool.frameNum,
              imgData: cCanData,
            })
            console.timeEnd('genWater time')
          })
      }
    },
    getFrame(num) {
      this.cCan_ctx.clearRect(0, 0, 960, 540)
      this.mCan_ctx.clearRect(0, 0, 960, 540)
      this.isEmpty = true
      this.frameSrc = this.host + '/api/frame/' + num
      if (this.$store.state.cWater_dic[num]) {
        this.annTool.isShowCWater = true
        this.cWater_ctx.putImageData(this.$store.getters.getCWater(num), 0, 0)
      } else {
        this.annTool.isShowCWater = false
      }
      if (this.$store.state.mCan_dic[num]) {
        this.mCan_ctx.putImageData(this.$store.getters.getMCan(num), 0, 0)
      }
      if (this.$store.state.cCan_dic[num]) {
        this.cCan_ctx.putImageData(this.$store.getters.getCCan(num), 0, 0)
      }
      //图片可能被缓存，所以必须send当前帧编号
      axios
        .post('/api/send/get_frame', { frameNum: num })
        .then(function (res) {})
    },
  },
  watch: {
    boxScale() {
      this.$nextTick(() => {
        this.boxHeight = this.$refs.canBox.getBoundingClientRect().height
      })
    },
    'annTool.frameNum': {
      handler(num) {
        this.getFrame(num)
      },
      deep: true,
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
.workspace__canvas {
  position: absolute;
  left: 0px;
  top: 0px;
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
