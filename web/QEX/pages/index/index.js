var app = getApp();
Page({
  data: {

  },
  onLoad: function () {
    app.editTabBar();
  },
  click1:function(){
    wx.navigateTo({
      url: '../regression/setting?model=BTC',
    })
  },
  click2: function () {
    wx.navigateTo({
      url: '../regression/setting?model=ETH',
    })
  },
  click3: function () {
    wx.navigateTo({
      url: '../regression/setting?model=EOS',
    })
  }


})