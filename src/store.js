import { createStore } from 'vuex'

export default createStore({
  state() {
    return {
      mask_canvas_dic: {},
      color_canvas_dic: {},
      color_water_dic: {},

      mask_canvas_undo_data: [],
      mask_canvas_redo_data: [],
      color_canvas_undo_data: [],
      color_canvas_redo_data: [],
    }
  },
  mutations: {
    canvas_redo_push() {
      color_canvas_undo_data.push(color_canvas_ctx.getImageData(0, 0, 960, 540))
      mask_canvas_undo_data.push(mask_canvas_ctx.getImageData(0, 0, 960, 540))
      if (color_canvas_undo_data.length > 100) {
        color_canvas_undo_data = color_canvas_undo_data.slice(50, -1)
        mask_canvas_undo_data = mask_canvas_undo_data.slice(50, -1)
      }
      $('.ann-tool__undo-length').text(color_canvas_undo_data.length)
    },
  },
})
