var swiper = new Swiper(".mySwiper", {
    speed: 600,
    parallax: true,
    spaceBetween: 30,
    loop:true,
    autoplay:{
        delay:5000,
    },
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
});


new Swiper(".achadossemana", {
  slidesPerView: 3,
  spaceBetween: 16,
  speed: 600,
  loop:true,
  breakpoints: {
    // quando a largura da viewport for 576 pixels ou mais
    576: {
      slidesPerView: 3,
      spaceBetween: 16
    },
    // quando a largura da viewport for 768 pixels ou mais
    768: {
      slidesPerView: 4,
      spaceBetween: 16
    },
    // quando a largura da viewport for 992 pixels ou mais
    992: {
      slidesPerView: 5,
      spaceBetween: 16
    },
    // quando a largura da viewport for 1200 pixels ou mais
    1200: {
      slidesPerView: 6,
      spaceBetween: 16
    }
  },
  autoplay:{
      delay:5000,
  },
  navigation: {
    nextEl: ".controle-next",
    prevEl: ".controle-prev",
  },
});

// API

$(document).ready(function(){
  $.get('/api-lista-prod-index/', { pg: 1 }, function(data) {
    $('.lista-produtos').html(data);
  });

  var page=2
  // Clicou ver mais
  $('.btn-vermais').click(function(){
    $.get('/api-lista-prod/', { pg: page }, function(data) {
      $('.lista-produtos').append(data);
      page++
    });
  })

  $('.btn-bars').click(function(){
    $('.mobile').toggleClass('open')

  })
  $('.btn-fechar').click(function(){
    $('.mobile').toggleClass('open')
  })

  $('.btn-filtro').click(function(){
    $('.filtros').toggleClass('open')

  })
  $('.btn-filtro-close').click(function(){
    $('.filtros').toggleClass('open')
  })

  $('.slide-img').hover(function() {
    $('.slide-img').removeClass('active'); // Remove 'active' class from all elements with class 'slide-img'
    $(this).toggleClass('active'); // Toggle 'active' class on the current element
    
    $('#img-prod').attr('src', $(this).find('.avatar-lg').attr('src')).slideDown(1000) 
  });

})