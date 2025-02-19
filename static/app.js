function locoScroll() {
  gsap.registerPlugin(ScrollTrigger);

  const locoScroll = new LocomotiveScroll({
    el: document.querySelector("#main"), // Ensure it matches your HTML
    smooth: true,
  });

  locoScroll.on("scroll", ScrollTrigger.update);

  ScrollTrigger.scrollerProxy("#main", {
    scrollTop(value) {
      return arguments.length
        ? locoScroll.scrollTo(value, 0, 0)
        : locoScroll.scroll.instance.scroll.y;
    },
    getBoundingClientRect() {
      return {
        top: 0,
        left: 0,
        width: window.innerWidth,
        height: window.innerHeight,
      };
    },
    pinType: document.querySelector("#main").style.transform
      ? "transform"
      : "fixed",
  });

  ScrollTrigger.addEventListener("refresh", () => locoScroll.update());
  ScrollTrigger.refresh();
}

function page2Animation() {
  gsap.from(".text h3", {
    x: -80,
    opacity: 0,
    duration: 1,
    stagger: 0.4,
    scrollTrigger: {
      trigger: "#page2",
      scroller: "#main",
      start: "top 44%",
      end: "top 40%",
      //   markers: true, // Debugging
      scrub: 2,
    },
  });

  gsap.from(".elem h1", {
    y: 180,
    stagger: 0.2,
    duration: 1.3,
    opacity: 0,
    scrollTrigger: {
      trigger: "#page2",
      scroller: "#main",
      start: "top 33%",
      end: "top 28%",
      //   markers: true, // Debugging
      scrub: 2,
    },
  });

  gsap.from(".line", {
    width: "0",
    stagger: 0.6,
    duration: 1,
    opacity: 0,
    scrollTrigger: {
      trigger: "#page2",
      scroller: "#main",
      start: "top 47%",
      end: "top 46%",
      //   markers: true, // Debugging
      scrub: 2,
    },
  });
}
function page3Animation() {
  gsap.from("h2", {
    y: 50,
    opacity: 0,
    scale: 0.8,
    stagger: 0.7,
    duration: 2,
    scrollTrigger: {
      trigger: ".explore",
      scroller: "#main",
      //   markers: true,
      scrub: 2,
      start: "top 70%",
      end: "top 57%",
    },
  });
}

var cursor = document.querySelector("#cursor");
var blur = document.querySelector("#c ursor-blur");
const nav = document.querySelectorAll("nav h3");
const team = document.querySelector(".team h3");
const teamc = document.querySelector(".names i");
const menuO = document.querySelector("#menut ");
const menuC = document.querySelector(".navmenu i");
function teamtimeline() {
  team.addEventListener("click", () => {
    tl.play();
  });
  teamc.addEventListener("click", () => {
    tl.reverse();
  });

  var tl = gsap.timeline({ paused: true });

  tl.to(".names", {
    left: 0,
    duration: 1.8,
  });

  tl.from(".names i", {
    opacity: 0,
    delay: 0.2,
  });
}

function cursroAnim() {
  nav.forEach((elem) => {
    elem.addEventListener("mouseenter", () => {
      gsap.to("#cursor", {
        scale: 3,
        border: "1px solid #fff",
        backgroundColor: "transparent",
      });
    });
    elem.addEventListener("mouseleave", () => {
      gsap.to("#cursor", {
        scale: 1,
        border: "0px solid #fff",
        backgroundColor: "#95c11e",
      });
    });
  });

  document.addEventListener("mousemove", (dets) => {
    const scrollContainer = document.querySelector("#main");
    const scrollY = scrollContainer
      ? scrollContainer.getBoundingClientRect().top
      : 0;

    gsap.to("#cursor", {
      x: dets.x + 30,
      y: dets.y - scrollY,
      delay: 0,
    });

    gsap.to("#cursor-blur", {
      x: dets.x - 150,
      y: dets.y - 150 - scrollY,
      delay: 0.1,
    });
  });
}

function cardAnim() {
  gsap.from(".card", {
    scale: 0.8,
    opacity: 0,
    duration: 1,
    //   stagger: 0.1,
    scrollTrigger: {
      trigger: ".card",
      scroller: "#main",
      //   markers: true,
      start: "top 65%",
      end: "top 58%",
      scrub: 1,
    },
  });
}

function quotAnim() {
  gsap.from("#colon1", {
    y: -80,
    x: -80,

    scrollTrigger: {
      trigger: "#colon1",
      scroller: "#main",
      //   markers: true,
      start: "top 46%",
      end: "top 34%",
      scrub: 1,
    },
  });
  gsap.from("#colon2", {
    y: 90,
    x: 90,

    scrollTrigger: {
      trigger: "#colon1",
      scroller: "#main",
      //   markers: true,
      start: "top 50%",
      end: "top 40%",
      scrub: 1,
    },
  });
}

function homeNav() {
  menuO.addEventListener("click", () => {
    console.log("hello");
    tl.play();
  });
  menuC.addEventListener("click", () => {
    tl.reverse();
  });
  var tl = gsap.timeline({ paused: true });

  tl.to(".navmenu", {
    right: 0,
    duration: 0.8,
  });
  tl.from(".navmenu h3", {
    x: 150,
    duration: 0.7,
    stagger: 0.28,
    opacity: 0,
  });
  tl.from(".navmenu i", {
    opacity: 0,
  });
}

function page7Animation() {
  const video = document.querySelector("#page7 video");

  video.addEventListener("mouseenter", () => {
    gsap.to("#cursor", {
      scale: 4,
      border: "1px solid #fff",
      backgroundColor: "transparent",
    });
  });
  video.addEventListener("mouseleave", () => {
    gsap.to("#cursor", {
      scale: 1,
      border: "0px solid #fff",
      backgroundColor: "#FF5F38",
    });
  });
}

locoScroll();
page2Animation();
cursroAnim();
page3Animation();
cardAnim();
quotAnim();
teamtimeline();
homeNav();
page7Animation();

function wheelAnim() {
  window.addEventListener("wheel", (dets) => {
    if (dets.deltaY > 0) {
      gsap.to(".marque", {
        transform: "translateX(-200%)",
        duration: 4,
        repeat: -1,
        ease: "none",
      });

      gsap.to(".marque img", {
        rotate: 180,
      });
    } else {
      gsap.to(".marque", {
        transform: "translateX(0%)",
        duration: 4,
        repeat: -1,
        ease: "none",
      });
      gsap.to(".marque img", {
        rotate: 0,
      });
    }
  });
}

wheelAnim();

var tl1 = gsap.timeline();
tl1.from("#loader h3", {
  x: 60,
  opacity: 0,
  duration: 1.3,
  stagger: 0.1,
});
tl1.to("#loader h3", {
  opacity: 0,
  x: -60,
  duration: 0.6,
  stagger: 0.1,
});

tl1.to("#loader", {
  opacity: 0,
});
tl1.from("#page1-content span", {
  y: 160,
  opacity: 0,
  stagger: 0.1,
  duration: 0.5,
  delay: -0.7,
});

tl1.to("#loader", {
  display: "none",
});
