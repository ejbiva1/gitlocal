var app = getApp();
var util = require('../../utils/util.js')
Page({
  data: {
    model:'',
    inputvalues : 'Initial Funding (USDT)',
    startDates:'Start Date',
    sysStartDate:'',
    sys2StartDate:'',
    sysEndDate: '',
    endDates:'End Date',
    pic_array: [
      { id: 1, name: '策略1' },
      { id: 2, name: '策略2' },
      { id: 3, name: '策略3' },
      { id: 4, name: '策略4' }
    ],
    hx_index: 0
  },
  onLoad: function (options) {
    app.editTabBar();
    var that = this;
    this.setData({
      model: options.model
    }),
    wx.setNavigationBarTitle({
      title: this.data.model+" / USDT",
    });

    if (this.data.model == "BTC"){
      this.setData({
        sysStartDate: "2017-10-27"
      })
    }
    else if(this.data.model == "ETC"){
      this.setData({
        sysStartDate: "2017-10-27"
      })
    }
    else{
      this.setData({
        sysStartDate: "2017-12-06"
      })
    }
    var date = new Date();
    var year = date.getFullYear();
    var month = date.getMonth()+1;
    var day = date.getDate()-2;
    this.setData({
      sysEndDate: year+"-"+month+"-"+day
    })
  },
  startTime: function (e) {
    console.log(e.detail.value)
    this.setData({
      startDates: e.detail.value,
      sys2StartDate: e.detail.value
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