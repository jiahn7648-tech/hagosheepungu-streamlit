import streamlit as st
# streamlit_p5 라이브러리를 사용합니다.
from streamlit_p5 import p5 

# --- Streamlit UI 및 설명 ---

st.set_page_config(page_title="2D 물리 엔진", layout="centered")

st.title("🍎 현실적인 2D 물리 엔진 시뮬레이션 (Matter.js & p5.js)")
st.markdown("---")
st.subheader("💡 상호작용 방법")
st.markdown("""
1.  **공 생성:** 화면 아무 곳이나 **마우스 왼쪽 버튼**을 클릭하면 공이 떨어집니다.
2.  **드래그:** 생성된 공을 **왼쪽 버튼**으로 클릭한 채 움직여 위치를 바꿀 수 있습니다.
3.  **충격:** 공을 잡고 빠르게 드래그한 후 놓으면, 속도가 적용되어 다른 공과 충돌하며 날아갑니다.
""")
st.markdown("---")

# --- Javascript (p5.js & Matter.js) 코드 ---

# 이 코드는 파이썬 코드가 아닌, 웹 브라우저에서 실행될 Javascript 코드입니다.
# 일반 문자열(triple quotes)로 정의하여 TypeError 발생을 방지합니다.
p5_code = """
// Matter.js 모듈 변수를 설정합니다.
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
let mConstraint; // 마우스 제약 (드래그 기능을 담당)

function setup() {
    // 캔버스 크기는 Streamlit 컴포넌트 호출 시 지정된 크기(600x400)를 따릅니다.
    createCanvas(600, 400); 

    // 1. 엔진 생성 및 중력 설정
    engine = Engine.create();
    world = engine.world;
    world.gravity.y = 1; // 중력 활성화 (아래로 떨어짐)

    // 2. 바닥 (벽) 생성
    // isStatic: 움직이지 않음
    ground = Bodies.rectangle(width / 2, height - 10, width, 20, { isStatic: true });
    World.add(world, ground);
    
    // 3. 마우스 드래그 기능 추가 (MouseConstraint)
    let canvasmouse = Mouse.create(canvas.elt);
    canvasmouse.pixelRatio = pixelDensity(); // 해상도 보정
    let options = {
        mouse: canvasmouse
    }
    // 마우스 입력과 물리 세계를 연결하여 드래그, 던지기 가능하게 합니다.
    mConstraint = MouseConstraint.create(engine, options);
    World.add(world, mConstraint);

    // 4. 러너 (물리 업데이트) 시작
    Runner.run(Runner.create(), engine);
}

function mouseClicked() {
    // 마우스 클릭 시 공 생성 (현재 드래그 중이 아닐 때만)
    if (!mConstraint.body) {
        // Bodies.circle(x, y, radius, [options])
        let newBall = Bodies.circle(mouseX, mouseY, 15, {
            restitution: 0.8, // 반발력 (탄성)
            friction: 0.001,  // 마찰
            density: 0.01     // 밀도
        });
        World.add(world, newBall);
    }
}

function draw() {
    background(220); // 배경색

    // 바닥 그리기
    fill(100);
    rectMode(CENTER);
    rect(ground.position.x, ground.position.y, width, 20);

    // 공 그리기
    let bodies = Composite.allBodies(world);

    for (let i = 0; i < bodies.length; i++) {
        let body = bodies[i];
        
        // 정적 오브젝트(바닥)는 그리지 않고 건너뜁니다.
        if (body.isStatic) continue; 

        let pos = body.position;
        let angle = body.angle;
        
        push(); 
        translate(pos.x, pos.y);
        rotate(angle);
        
        fill(255, 0, 100); // 공 색상
        ellipse(0, 0, body.circleRadius * 2); 
        
        pop(); 
    }
    
    // 마우스 드래그 연결선 그리기 (선택 사항)
    if (mConstraint.body) {
        let pos = mConstraint.body.position;
        let offset = mConstraint.constraint.pointB;
        let m = mConstraint.mouse.position;
        
        stroke(0, 255, 0); 
        line(pos.x + offset.x, pos.y + offset.y, m.x, m.y);
    }
}
"""

# --- Streamlit 컴포넌트 호출 ---
# app.py의 마지막 라인 (이전 오류 이미지에서 Line 126에 해당)
p5(p5_code, width=600, height=400)
