<template>
  <cv-collapse-item :name="name">
    <template v-slot:header>
      <div>cv2.GaussianBlur</div>
    </template>

    <el-form ref="form" :model="argForm" label-width="80px" size="mini">
      <el-form-item label="活动名称">
        <el-input v-model="argForm.name"></el-input>
      </el-form-item>
      <el-form-item label="活动区域">
        <el-select v-model="argForm.region" placeholder="请选择活动区域">
          <el-option label="区域一" value="shanghai"></el-option>
          <el-option label="区域二" value="beijing"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="活动时间">
        <el-col :span="11">
          <el-date-picker
            type="date"
            placeholder="选择日期"
            v-model="argForm.date1"
            style="width: 100%"
          ></el-date-picker>
        </el-col>
        <el-col class="line" :span="2">-</el-col>
        <el-col :span="11">
          <el-time-picker
            placeholder="选择时间"
            v-model="argForm.date2"
            style="width: 100%"
          ></el-time-picker>
        </el-col>
      </el-form-item>
      <el-form-item label="活动性质">
        <el-checkbox-group v-model="argForm.type">
          <el-checkbox-button
            label="美食/餐厅线上活动"
            name="type"
          ></el-checkbox-button>
          <el-checkbox-button label="地推活动" name="type"></el-checkbox-button>
          <el-checkbox-button
            label="线下主题活动"
            name="type"
          ></el-checkbox-button>
        </el-checkbox-group>
      </el-form-item>
      <el-form-item label="特殊资源">
        <el-radio-group v-model="argForm.resource" size="medium">
          <el-radio border label="线上品牌商赞助"></el-radio>
          <el-radio border label="线下场地免费"></el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">立即创建</el-button>
        <el-button>取消</el-button>
      </el-form-item>
    </el-form>
  </cv-collapse-item>
</template>

<script>
import CvCollapseItem from './CvCollapseItem.vue'
export default {
  data() {
    return {
      argForm: {
        name: '',
        region: '',
        date1: '',
        date2: '',
        delivery: false,
        type: [],
        resource: '',
        desc: '',
      },
    }
  },
  props: {
    name: String,
    argForm0: {
      type: Object,
      // 对象或数组默认值必须从一个工厂函数获取
      default() {
        return {
          name: '',
          region: '',
          date1: '',
          date2: '',
          delivery: false,
          type: [],
          resource: '',
          desc: '',
        }
      },
    },
  },
  emits: ['update:argForm'],
  components: {
    CvCollapseItem,
  },
  methods: {
    onSubmit() {
      console.log('submit!')
    },
  },
  watch: {
    argForm: {
      handler(val, oldVal) {
        this.$emit('update:argForm', val)
        console.log('funcCut', val)
      },
      deep: true,
    },
  },
}
</script>

<style scoped>
</style>
