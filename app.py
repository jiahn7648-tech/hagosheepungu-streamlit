import streamlit as st
import pymunk
import matplotlib.pyplot as plt
import numpy as np
import time 

# 상수 설정
DT = 1/60.0  # 물리 시간 간격 (60 FPS)
FRAME_COUNT = 300 # 전체 애니메이션 프레임 수 (약 5초)
BALL_RADIUS = 10
WIDTH = 500
HEIGHT = 500

# --- Pymunk 초기화 (앱 시작 시 한 번만 실행) ---
def initialize_physics():
    space = pymunk.Space()
    space.gravity = (0, 0)
    st.session_state.space = space
    st.session_state.balls = []
    
    # 경계 벽 추가 (화면 밖으로 나가지 않도록)
    add_boundaries(space, WIDTH, HEIGHT)

def create_ball(position, radius=BALL_RADIUS, mass=1, elasticity=0.9):
    # 강체 (Body): 물리적 속성
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment)
    body.position = position

    # 모양 (Shape): 충돌 감지 영역
    shape = pymunk.Circle(body, radius)
    shape.elasticity = elasticity
    shape.density = 1

    st.session_state.space.add(body, shape)
    return body

def setup_balls(num_balls):
    # 매번 새로운 시뮬레이션을 위해 초기화
    initialize_physics() 
    
    balls = []
    for i in range(num_balls):
        # 공을 중앙 가로선에 일렬로 배치
        pos = (i * (2*BALL_RADIUS + 5) + 50, HEIGHT / 2) 
        ball = create_ball(pos)
        balls.append(ball)
    st.session_state.balls = balls

def add_boundaries(space, width, height):
    static_body = space.static_body
    
    # 4면의 벽 세그먼트
    walls = [
        pymunk.Segment(static_body, (0, 0), (width, 0), 1),      # 아래
        pymunk.Segment(static_body, (0, 0), (0, height), 1),    # 왼쪽
        pymunk.Segment(static_body, (width, 0), (width, height), 1),  # 오른쪽
        pymunk.Segment(static_body, (0, height), (width, height), 1), # 위
    ]
    
    for wall in walls:
        wall.elasticity = 0.95 # 벽에 부딪히면 튕기기
        space.add(wall)

# --- 시뮬레이션 한 프레임 실행 및 그리기 ---
def simulate_and_draw(frame_counter):
    space = st.session_state.space
    balls = st.session_state.balls
    
    # 첫 프레임(0)에서만 공에 충격(임펄스)을 가함
    if frame_counter == 0 and not st.session_state.initial_hit_applied:
        hit_index = st.session_state.hit_ball_index
        if hit_index < len(balls):
            ball_to_hit = balls[hit_index]
            # 오른쪽으로 강한 충격량 적용 (움직임을 시작)
            ball_to_hit.apply_impulse_at_local_point((10000, 0), (0, 0)) 
            st.session_state.initial_hit_applied = True
    
    # 물리 스텝 진행
    space.step(DT)
    
    # 시각화 (Matplotlib)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, HEIGHT)
    ax.set_aspect('equal')
    ax.set_title(f"충돌 시뮬레이션 (프레임: {frame_counter})")

    for i, body in enumerate(balls):
        x, y = body.position
        
        # 공 그리기 (충격 받은 공은 빨간색으로 표시)
        color = 'red' if i == st.session_state.hit_ball_index else 'blue'
        circle = plt.Circle((x, y), BALL_RADIUS, color=color, fill=True)
        ax.add_artist(circle)
        
    return fig

# --- Streamlit UI 구성 ---

st.title("🎱 드래그 및 충돌 물리 시뮬레이션")
st.markdown("---")

# 세션 상태 초기화
if 'simulation_ready' not in st.session_state:
    st.session_state.simulation_ready = False
    st.session_state.initial_hit_applied = False
    st.session_state.num_balls = 5
    st.session_state.hit_ball_index = 0
    initialize_physics()


col1, col2 = st.columns(2)
with col1:
    st.session_state.num_balls = st.slider("공의 개수", 2, 10, st.session_state.num_balls, key='num_slider')
with col2:
    st.session_state.hit_ball_index = st.number_input(
        "충격을 가할 공 번호 (0부터 시작)", 
        0, 
        st.session_state.num_balls - 1 if st.session_state.num_balls > 0 else 0, 
        st.session_state.hit_ball_index,
        key='hit_slider'
    )

if st.button("시뮬레이션 시작"):
    # 설정에 따라 공들을 다시 배치
    setup_balls(st.session_state.num_balls)
    st.session_state.simulation_ready = True
    st.session_state.initial_hit_applied = False
    
st.markdown("---")

if st.session_state.simulation_ready:
    
    # 애니메이션이 표시될 영역
    placeholder = st.empty()
    
    # 프레임 수만큼 반복하며 움직임 표시
    for frame in range(FRAME_COUNT):
        # 1. 현재 프레임의 물리 계산 및 그림 생성
        fig = simulate_and_draw(frame)
        
        # 2. 그림 표시 (이전 그림을 덮어씀)
        with placeholder:
            st.pyplot(fig)
            plt.close(fig) # 메모리 누수 방지를 위해 그림 닫기
            
        # 3. 프레임 간격만큼 대기 (애니메이션 속도 조절)
        time.sleep(DT)
        
    # 최종 상태 표시
    st.success("충돌 시뮬레이션이 완료되었습니다.")
    st.session_state.simulation_ready = False # 시뮬레이션 상태 초기화
    
else:
    st.info("공의 개수와 충격을 가할 공을 선택하고 '시뮬레이션 시작' 버튼을 눌러주세요.")
