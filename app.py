import streamlit as st
from streamlit_p5 import p5 

st.set_page_config(page_title="2D 물리 엔진", layout="centered")

st.title("🍎 현실적인 2D 물리 엔진 시뮬레이션")
st.markdown("---")
st.markdown("화면을 클릭하여 공을 생성하고, 드래그하여 움직이거나 던져보세요. 중력과 충돌이 적용됩니다.")

# Javascript (p5.js & Matter.js) 코드
p5_code = """
let Engine = Matter.Engine,
    Render = Matter.Render,
    Runner = Matter.Runner,
    Bodies = Matter.Bodies,
    Composite = Matter.Composite,
    MouseConstraint = Matter.MouseConstraint,
    Mouse = Matter.Mouse,
    World = Matter.World;

let engine;
let world;
let ground;
let mConstraint;

function setup() {
    createCanvas(600, 400); 

    engine = Engine.create();
    world = engine.world;
    world.gravity.y = 1; 

    ground = Bodies.rectangle(width / 2, height - 10, width, 20, { isStatic: true });
    World.add(world, ground);
    
    let canvasmouse = Mouse.create(canvas.elt);
    canvasmouse.pixelRatio = pixelDensity(); 
    let options = { mouse: canvasmouse }
    
    mConstraint = MouseConstraint.create(engine, options);
    World.add(world, mConstraint);

    Runner.run(Runner.create(), engine);
}

function mouseClicked() {
    if (!mConstraint.body) {
        let newBall = Bodies.circle(mouseX, mouseY, 15, {
            restitution: 0.8, 
            friction: 0.001,  
            density: 0.01     
        });
        World.add(world, newBall);
    }
}

function draw() {
    background(220);

    fill(100);
    rectMode(CENTER);
    rect(ground.position.x, ground.position.y, width, 20);

    let bodies = Composite.allBodies(world);

    for (let i = 0; i < bodies.length; i++) {
        let body = bodies[i];
        
        if (body.isStatic) continue; 

        let pos = body.position;
        let angle = body.angle;
        
        push(); 
        translate(pos.x, pos.y);
        rotate(angle);
        
        fill(255, 0, 100);
        ellipse(0, 0, body.circleRadius * 2); 
        
        pop(); 
    }
    
    if (mConstraint.body) {
        let pos = mConstraint.body.position;
        let offset = mConstraint.constraint.pointB;
        let m = mConstraint.mouse.position;
        
        stroke(0, 255, 0); 
        line(pos.x + offset.x, pos.y + offset.y, m.x, m.y);
    }
}
"""

# Streamlit 컴포넌트 호출 (오류가 나는 바로 그 줄)
p5(p5_code, width=600, height=400)
