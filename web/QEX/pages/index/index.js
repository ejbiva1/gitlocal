var app = getApp();
Page({
  data: {

  },
  onLoad: function () {
    app.editTabBar();
  },
  click:function(){
    wx.navigateTo({
      url: '../regression/setting',
    })
  }


})