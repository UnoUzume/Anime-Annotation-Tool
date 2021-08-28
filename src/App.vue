<template>
  <el-container style="height: 100%">
    <el-header class="page-header" height="36px">
      <el-row align="middle">
        <el-col :span="24">
          <el-button type="text" size="mini" icon="el-icon-edit"
            >菜单</el-button
          >
          <el-button type="text" size="mini" icon="el-icon-share"
            >保存</el-button
          >
          <el-button type="text" size="mini" icon="el-icon-delete"
            >撤销</el-button
          >
          <el-button type="text" size="mini" icon="el-icon-search"
            >重做</el-button
          >
          <el-button type="text" size="mini"
            >上传<i class="el-icon-upload el-icon--right"></i
          ></el-button>
        </el-col>
      </el-row>
    </el-header>
    <el-container class="page-body">
      <el-aside class="page-body__left" width="200px">
        <div class="ann-label__box">
          <div
            class="ann-label__item"
            v-for="label in label_list"
            :key="label.id"
          >
            <div class="ann-label__color"></div>
            <span class="ann-label__id">{{ label.id }}</span>
            <input
              type="text"
              class="ann-label__name"
              readonly
              :value="label.name"
            />
          </div>
        </div>
      </el-aside>
      <el-container>
        <el-header class="workspace__header" height="54px">
          <el-row align="middle">
            <el-col :span="24">
              <el-button size="mini">上一帧</el-button>
              <el-button size="mini">下一帧</el-button>
              <el-button size="mini">步退</el-button>
              <el-button size="mini">步进</el-button>
              <el-button size="mini">上一关键帧</el-button>
              <el-button size="mini">下一关键帧</el-button>
              <el-form
                :inline="true"
                :model="formInline"
                class="workspace__header-form"
                size="mini"
              >
                <el-form-item label="当前帧">
                  <el-input-number
                    v-model="frameNum"
                    controls-position="right"
                    @change="handleChange"
                    :min="0"
                  ></el-input-number>
                </el-form-item>
                <el-form-item label="步长">
                  <el-input-number
                    v-model="frameStep"
                    controls-position="right"
                    @change="handleChange"
                    :min="1"
                  ></el-input-number>
                </el-form-item>
              </el-form>
            </el-col>
          </el-row>
        </el-header>
        <el-main class="workspace">
          <div class="workspace__canvas-wrapper">
            <div
              class="workspace__canvas-box"
              data-is-moving="false"
              data-xc="0"
              data-yc="0"
            >
              <!-- src="{{ url_for('static', filename = 'images/canvas.png' ) }}" -->
              <img class="workspace__frame" src="/static/canvas.png" alt="" />
              <canvas
                class="workspace__color-water"
                width="960"
                height="540"
              ></canvas>
              <canvas
                class="workspace__mask-canvas"
                width="960"
                height="540"
              ></canvas>
              <canvas
                class="workspace__color-canvas"
                width="960"
                height="540"
              ></canvas>
            </div>
            <div class="workspace__cursor">
              <svg xmlns="http://www.w3.org/2000/svg" version="1.1">
                <rect width="20" height="20"></rect>
              </svg>
            </div>
          </div>
        </el-main>
        <el-footer class="workspace__footer" height="120px"> </el-footer>
      </el-container>
      <el-aside class="page-body__right" width="320px">
        <el-scrollbar>
          <cv-func v-model="cvFunc" />
        </el-scrollbar>
      </el-aside>
    </el-container>
  </el-container>
</template>

<script>
import CvFunc from './components/CvFunc.vue'
import CvCollapse from './components/CvCollapse.vue'
import CvCollapseItem from './components/CvCollapseItem.vue'
export default {
  data() {
    return {
      cvFunc: [
        { func: 'paint', name: 'func1' },
        { func: 'cut', name: 'func2' },
      ],
      frameNum: 0,
      frameStep: 0,
      formInline: {
        user: '',
        region: '',
      },
      label_list: [
        { id: '250', name: 'background', bgc: '4e4e4e' },
        { id: '1', name: '四之宫京夜', bgc: '7c527b' },
        { id: '2', name: '天使真央', bgc: 'ff9f50' },
        { id: '3', name: '天使惠', bgc: 'ff8dad' },
        { id: '4', name: '皇紫音', bgc: 'a47fd6' },
        { id: '5', name: '绮罗罗·伯恩斯坦', bgc: 'ffe09e' },
        { id: '6', name: '神无月环', bgc: '9ce06f' },
      ],
      show3: true,
      activeNames: [],
      checked: true,
      checked2: true,
    }
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
  },
  components: {
    CvFunc,
    CvCollapse,
    CvCollapseItem,
  },
}
</script>

<style>
html,
body,
#app {
  height: 100%;
  width: 100%;
  margin: 0px;
  background: #f5f6f8;
}
.page-header .el-button {
  font-size: 1rem;
}
.el-button {
  padding: 0px 7px;
}
.workspace__header-form {
  display: inline-block;
}
.el-form-item {
  margin-bottom: 5px !important;
}
.workspace__header-form .el-input-number {
  width: 5em;
}
.el-input-number.is-controls-right .el-input__inner {
  padding-left: 0px !important;
  padding-right: 30px !important;
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

.workspace {
  /* width: 0px; */
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
  background-color: #9ce06f;
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
