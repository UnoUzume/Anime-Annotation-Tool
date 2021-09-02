<template>
  <el-container style="height: 100%">
    <el-header class="page-header" height="28px">
      <el-row align="middle" style="width: 100%">
        <el-col :span="8">
          <el-button type="text" icon="el-icon-edit">菜单</el-button>
          <el-button type="text" icon="el-icon-share">保存</el-button>
          <el-button type="text" icon="el-icon-delete">撤销</el-button>
          <el-button type="text" icon="el-icon-search">重做</el-button>
        </el-col>
        <el-col :span="16">
          <label>笔刷大小</label>
          <input type="number" min="1" max="50" v-model="annTool.brushSize" />
          <label>画布</label>
          <input
            type="number"
            min="0"
            max="1"
            step="0.1"
            v-model="annTool.cCanAlpha"
          />
          <input type="checkbox" v-model="annTool.isShowCCan" />
          <label>分割结果</label>
          <input
            type="number"
            min="0"
            max="1"
            step="0.1"
            v-model="annTool.cWaterAlpha"
          />
          <input type="checkbox" v-model="annTool.isShowCWater" />
          <el-button @click="canvasResize">重置画布</el-button>
          <el-button @click="canvasClear">清空画布</el-button>
          <el-button @click="canvasUndo">撤销 {{ undoLength }}</el-button>
          <el-button @click="canvasRedo">反撤销 {{ redoLength }}</el-button>
          <el-button @click="genWater">生成分割</el-button>
        </el-col>
      </el-row>
    </el-header>
    <el-container class="page-body">
      <el-aside class="page-body__left" width="200px">
        <div class="ann-label__box">
          <div
            class="ann-label__item"
            :class="{ active: label.id == activeLabel.id }"
            v-for="label in labelList"
            :key="label.id"
            @click="whenClickLabel(label)"
          >
            <div
              class="ann-label__color"
              :style="{ backgroundColor: '#' + label.bgc }"
            ></div>
            <span class="ann-label__id">{{ label.id }}</span>
            <input
              type="text"
              class="ann-label__name"
              readonly
              :value="label.name"
            />
          </div>
        </div>
        <div style="color: royalblue">
          <span v-if="keyframes">已加载keyframes</span>
          <span v-else-if="gettingKeyframes"> 正在获取keyframes...</span>
          <template v-else>
            <span>未找到keyframes信息</span>
            <button type="button" @click="genKeyframes">生成keyframes</button>
          </template>
        </div>
        <textarea
          class="page-body__output"
          readonly
          v-model="outputText"
          ref="output"
        ></textarea>
      </el-aside>
      <el-container>
        <el-header class="workspace__header" height="54px">
          <el-row align="middle">
            <el-col :span="24">
              <el-button @click="annTool.frameNum--">上一帧</el-button>
              <el-button @click="annTool.frameNum++">下一帧</el-button>
              <el-button @click="annTool.frameNum -= annTool.frameStep"
                >步退</el-button
              >
              <el-button @click="annTool.frameNum += annTool.frameStep"
                >步进</el-button
              >
              <el-button @click="preKeyframe">上一关键帧</el-button>
              <el-button @click="nextKeyframe">下一关键帧</el-button>
              <el-form :inline="true" style="display: inline-block" size="mini">
                <el-form-item label="当前帧">
                  <el-input-number
                    v-model="annTool.frameNum"
                    controls-position="right"
                    :min="0"
                  ></el-input-number>
                </el-form-item>
                <el-form-item label="步长">
                  <el-input-number
                    v-model="annTool.frameStep"
                    controls-position="right"
                    :min="1"
                  ></el-input-number>
                </el-form-item>
              </el-form>
              <el-radio-group v-model="jumpMethod">
                <el-radio-button label="0">跳帧</el-radio-button>
                <el-radio-button label="1">跳步</el-radio-button>
                <el-radio-button label="2">跳关键帧</el-radio-button>
              </el-radio-group>
            </el-col>
          </el-row>
        </el-header>
        <el-main class="workspace">
          <work-space ref="workSpace" />
        </el-main>
        <el-footer class="workspace__footer" height="120px">
          <e-charts ref="eCharts" />
        </el-footer>
      </el-container>
      <el-aside class="page-body__right" width="250px">
        <el-container style="height: 100%">
          <el-header height="130px">
            <div class="mouse-info" ref="mouseInfo"></div>
          </el-header>
          <el-main>
            <el-scrollbar>
              <cv-func v-model="cvFunc" />

              <el-button @click="showfunc">下一关键帧</el-button>
            </el-scrollbar>
          </el-main>
          <el-footer height="30px">Footer</el-footer>
        </el-container>
      </el-aside>
    </el-container>
  </el-container>
</template>

<script>
import { ref, reactive, computed } from 'vue'
import axios from 'axios'
import CvFunc from './components/CvFunc.vue'
import CvCollapse from './components/CvCollapse.vue'
import CvCollapseItem from './components/CvCollapseItem.vue'
import WorkSpace from './components/WorkSpace.vue'
import ECharts from './components/ECharts.vue'
export default {
  components: {
    CvFunc,
    CvCollapse,
    CvCollapseItem,
    WorkSpace,
    ECharts,
  },
  data() {
    return {
      cvFunc: [
        {
          func: 'cut',
          name: 'func1',
          argForm: {},
        },
        {
          func: 'cut',
          name: 'func2',
          argForm: {},
        },
        {
          func: 'cut',
          name: 'func3',
          argForm: {},
        },
      ],
      jumpMethod: 2,
      annTool: {
        brushSize: 20,
        cCanAlpha: 0.7,
        isShowCCan: true,
        cWaterAlpha: 0.7,
        isShowCWater: true,
        frameNum: 0,
        frameStep: 3,
      },
      activeLabel: {},
      labelList: [],
      value1: 1,
      labelKeyMap: {
        f: 0,
        q: 1,
        w: 2,
        e: 3,
        r: 4,
        z: 5,
        x: 6,
        c: 7,
        v: 8,
      },
      keyframes: [],
      gettingKeyframes: false,
      outputText: '',
    }
  },
  inject: ['host'],
  computed: {
    undoLength() {
      return this.$store.state.cCan_undoL.length - 1
    },
    redoLength() {
      return this.$store.state.cCan_redoL.length
    },
    cusorStyle() {
      return {
        transform: `translate(-50%, -50%) scale(${this.cusorScale})`,
        width: this.annTool.brushSize + 'px',
        height: this.annTool.brushSize + 'px',
      }
    },
  },
  methods: {
    onSubmit() {
      console.log('submit!')
    },
    handleChange(value) {
      console.log(value)
    },
    doThis(val) {
      console.log('doThis!' + val)
    },
    showfunc() {
      console.log(this.cvFunc)
    },
    whenClickLabel(label) {
      //https://www.jianshu.com/p/94935f134741
      Object.assign(this.activeLabel, label)
    },
    canvasClear() {
      this.$refs.workSpace.canvasClear()
    },
    canvasResize() {
      this.$refs.workSpace.canvasResize()
    },
    canvasUndo() {
      this.$refs.workSpace.canvasUndo()
    },
    canvasRedo() {
      this.$refs.workSpace.canvasRedo()
    },
    genWater() {
      this.$refs.workSpace.genWater()
    },
    preKeyframe() {
      if (!this.keyframes) return this.output('no keyframe')
      // this.annTool.frameNum = this.keyframes
      //   .reverse()
      //   .find((value) => value < this.annTool.frameNum)
      let index = this.keyframes.findIndex(
        (value) => value > this.annTool.frameNum - 1
      )
      this.annTool.frameNum =
        this.keyframes[index > 0 ? index - 1 : this.keyframes.length - 1]
    },
    nextKeyframe() {
      if (!this.keyframes) return this.output('no keyframe')
      let num = this.keyframes.find((value) => value > this.annTool.frameNum)
      this.annTool.frameNum = num ? num : this.keyframes[0]
    },
    output(str) {
      this.outputText += str + '\n'
      this.$refs.output.scrollTop = this.$refs.output.scrollHeight
    },
    genKeyframes() {
      this.gettingKeyframes = true
      var source = new EventSource(this.host + '/api/ana_keyframes')
      source.onmessage = (e) => this.output(e.data)
      source.onerror = (e) => {
        source.close()
        this.output('source.error')
      }
      source.addEventListener('yield_end', (e) => {
        source.close()
        this.output(e.data)
        this.output('yield_end')
        // get_frame(parseInt($('.workspace__frame-num').val()))
        axios
          .post('/api/get', { keys: ['keyframes'] })
          .then((res) => (this.keyframes = res.data.keyframes))
        this.$refs.eCharts.initData()
      })
    },
  },
  provide() {
    return {
      annTool: this.annTool,
      activeLabel: this.activeLabel,
    }
  },
  mounted() {
    axios.post('/api/get', { keys: ['keyframes', 'labelList'] }).then((res) => {
      this.keyframes = res.data.keyframes
      this.labelList = res.data.labelList
      this.whenClickLabel(this.labelList[0])
      this.annTool.frameNum = 1
      this.annTool.frameNum = 0
    })
    document.addEventListener('mousemove', (e) => {
      this.$refs.mouseInfo.innerHTML =
        `clientX${e.clientX},clientY${e.clientY}<br>` +
        `screenX:${e.screenX},screenY${e.screenY}<br>` +
        `pageX:${e.pageX},pageY:${e.pageY}<br>` +
        `offsetX:${e.offsetX},offsetY${e.offsetY}<br>` +
        `x:${e.x},y:${e.y}<br>` +
        `movementX:${e.movementX},movementY:${e.movementY}`
    })
    document.addEventListener('keydown', (e) => {
      // console.log(e)
      if (!e.repeat) this.output('keydown: ' + e.key)
      if (e.key in this.labelKeyMap) {
        this.whenClickLabel(this.labelList[this.labelKeyMap[e.key]])
      } else if (e.key == ' ') {
        this.genWater()
      } else if (e.key == 'a') {
        if (this.jumpMethod == 0) this.annTool.frameNum--
        else if (this.jumpMethod == 1)
          this.annTool.frameNum -= this.annTool.frameStep
        else this.preKeyframe()
      } else if (e.key == 'd') {
        if (this.jumpMethod == 0) this.annTool.frameNum++
        else if (this.jumpMethod == 1)
          this.annTool.frameNum += this.annTool.frameStep
        else this.nextKeyframe()
      } else if (e.key == 'g') {
        this.canvasClear()
      } else if (e.key == 's') {
        this.annTool.isShowCWater = !this.annTool.isShowCWater
      } else {
        return
      }
    })
  },
}
</script>

<style>
*,
*::before,
*::after {
  box-sizing: border-box;
}
html,
body,
#app {
  height: 100%;
  width: 100%;
  margin: 0px;
  background: #f5f6f8;
}
input[type='number'] {
  width: 3.5em;
  height: 20px;
}
.page-header {
  font-size: 14px;
  line-height: 1;
}
.el-button.el-button--text {
  font-size: 16px;
}
.el-button {
  min-height: 20px;
  padding: 0px 7px;
  font-size: 12px;
  border-radius: calc(var(--el-border-radius-base) - 1px);
}
.el-button + .el-button {
  margin-left: 6px;
}
.el-form-item {
  margin-bottom: 5px !important;
}
.el-input-number {
  width: 5em;
}
.el-input-number.is-controls-right .el-input__inner {
  padding-left: 0px !important;
  padding-right: 30px !important;
}
.el-radio-button__inner {
  min-height: 20px;
  padding: 0px 7px;
  line-height: 20px;
  font-size: 12px;
  background-color: #fff;
}
.page-header {
  display: flex;
  background: #d8d8d8;
}

.page-body {
  height: 0px;
}
.page-body__left {
  border-right: 1px solid #c3c3c3;
}
.page-body__right {
  border-left: 1px solid #c3c3c3;
}
.el-aside,
.el-main,
.el-header,
.el-footer {
  position: relative;
  padding: 0px;
}

.workspace__header {
  border-bottom: 1px solid #c3c3c3;
}
.workspace__footer {
  border-top: 1px solid #c3c3c3;
}

.ann-label__item {
  display: flex;
  align-items: center;
  margin: 5px;
  border: grey 1px solid;
  border-left-width: 10px;
  padding: 5px;
  font-size: 12px;
}
.ann-label__item.active {
  border-color: royalblue;
}
.ann-label__item .ann-label__color {
  flex: none;
  height: 30px;
  width: 30px;
  background-color: #505050;
  display: inline;
}
.ann-label__item .ann-label__name {
  flex: auto;
  margin: 5px;
  width: 0px;
}
.ann-label__item .ann-label__id {
  flex: none;
  margin: 0px 6px;
  width: 2em;
  text-align: center;
}
/* .cv-collapse-item__header {
  height: 20px;
  line-height: 20px;
  border-bottom-color: #c3c3c3;
} */
.el-collapse-item__content {
  padding: 0px;
}
.el-collapse {
  --el-collapse-border-color: #c3c3c3;
  --el-collapse-header-height: 24px;
  --el-collapse-header-background-color: inherit;
  /* --el-collapse-header-font-color: var(--el-text-color-primary);
  --el-collapse-header-font-size: 13px;
  --el-collapse-content-background-color: var(--el-color-white);
  --el-collapse-content-font-size: 13px;
  --el-collapse-content-font-color: var(--el-text-color-primary); */
  border-top: 1px solid #c3c3c3;
  border-bottom: 1px solid #c3c3c3;
}
.el-slider {
  --el-slider-main-background-color: var(--el-color-primary);
  --el-slider-runway-background-color: var(--el-border-color-light);
  --el-slider-stop-background-color: var(--el-color-white);
  --el-slider-disable-color: var(--el-text-color-placeholder);
  --el-slider-margin: 8px 0;
  --el-slider-border-radius: 3px;
  --el-slider-height: 4px;
  --el-slider-button-size: 14px;
  --el-slider-button-wrapper-size: 24px;
  --el-slider-button-wrapper-offset: -10px;
}

.mouse-info {
  width: 100%;
  height: 130px;
  background-color: rgb(194, 230, 253);
  line-height: 20px;
}
.page-body__output {
  position: absolute;
  height: 200px;
  width: calc(100% - 10px);
  margin: 5px;
  bottom: 0px;
  resize: none;
}
</style>
