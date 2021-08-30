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
            :class="{ active: label.id == active_label.id }"
            v-for="label in label_list"
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

        <label>
          笔刷大小：
          <input
            type="number"
            name="frame-num"
            min="1"
            max="50"
            v-model="annTool.brushSize"
          />
        </label>
        <br />
        <label>
          画布透明度：
          <input type="number" value="0.7" min="0" max="1" step="0.1" />
        </label>
        <br />
        <label>
          画布显示：
          <input
            type="checkbox"
            class="ann-tool__color-canvas-visible"
            checked
          />
        </label>
        <br />
        <label>
          分割结果透明度：
          <input
            type="number"
            class="ann-tool__color-water-alpha"
            value="0.7"
            min="0"
            max="1"
            step="0.1"
          />
        </label>
        <br />
        <label>
          分割结果显示：
          <input
            type="checkbox"
            class="ann-tool__color-water-visible"
            checked
          />
        </label>
        <br />

        <el-button size="mini" class="ann-tool__canvas-resize"
          >重置画布大小和位置</el-button
        >
        <el-button size="mini" class="ann-tool__canvas-clear"
          >清空画布</el-button
        >
        <br />
        <el-button size="mini" class="ann-tool__canvas-undo">撤销</el-button>
        <el-button size="mini" class="ann-tool__canvas-redo">反撤销</el-button>
        <br />
        <span>
          撤销队列：
          <span class="ann-tool__undo-length">0</span>
        </span>
        <span>
          反撤销队列：
          <span class="ann-tool__redo-length">0</span>
        </span>
        <br />
        <el-button size="mini" class="ann-tool__canvas-gen-water"
          >生成分割</el-button
        >
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
          <work-space />
        </el-main>
        <el-footer class="workspace__footer" height="120px"> </el-footer>
      </el-container>
      <el-aside class="page-body__right" width="320px">
        <el-scrollbar>
          <cv-func v-model="cvFunc" />

          <el-button size="mini" @click="showfunc">下一关键帧</el-button>
        </el-scrollbar>
      </el-aside>
    </el-container>
  </el-container>
</template>

<script>
import { reactive } from 'vue'
import CvFunc from './components/CvFunc.vue'
import CvCollapse from './components/CvCollapse.vue'
import CvCollapseItem from './components/CvCollapseItem.vue'
import WorkSpace from './components/WorkSpace.vue'
export default {
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
      ],
      frameNum: 0,
      frameStep: 0,
      formInline: {
        user: '',
        region: '',
      },
      annTool: { brushSize: 20 },
      active_label: { id: '10', name: '神无月环', bgc: '9ce06f' },
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
      value1: 1,
    }
  },
  provide() {
    return {
      annTool: this.annTool,
      active_label: this.active_label,
    }
  },
  created() {
    this.$nextTick(() => {
      this.whenClickLabel(this.label_list[0])
    })
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
      Object.assign(this.active_label, label)
    },
  },
  components: {
    CvFunc,
    CvCollapse,
    CvCollapseItem,
    WorkSpace,
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
  min-height: 20px;
  padding: 0px 7px;
}
.el-button + .el-button {
  margin-left: 6px;
}
.workspace__header-form {
  display: inline-block;
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
</style>
