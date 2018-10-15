var app = getApp();
var util = require('../../utils/util.js')
Page({
  data: {
    inputvalues : '',
    startDates:'Start Date',
    endDates:'End Date',
    pic_array: [
      { id: 1, name: '策略1' },
      { id: 2, name: '策略2' },
      { id: 3, name: '策略3' },
      { id: 4, name: '策略4' }
    ],
    hx_index: 0
  },
  onLoad: function () {
    app.editTabBar();
    
  },
  startTime: function (e) {
    console.log(e.detail.value)
    this.setData({
      startDates: e.detail.value
    })
  },
  endTime: function (e) {
    console.log(e.detail.value)
    this.setData({
      endDates: e.detail.value
    })
  },
  inputs: function (e) {
    var v1 = e.detail.value;
    this.setData({
      inputvalues : v1,
    })
  },
  bindButtonTap: function (e){
    wx.navigateTo({
      url: "currentDetail"
    })
  },
  bindPickerChange_hx: function (e) {
    console.log('picker发送选择改变，携带值为', e.detail.value);
    this.setData({   //给变量赋值
      hx_index: e.detail.value,  //每次选择了下拉列表的内容同时修改下标然后修改显示的内容，显示的内容和选择的内容一致
    })
    console.log('自定义值:', this.data.hx_select);
  },
})