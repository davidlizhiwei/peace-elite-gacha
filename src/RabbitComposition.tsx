import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";

// 小草组件 - 会随风轻轻摇摆
const Grass: React.FC<{ x: number; delay: number; height: number }> = ({ x, delay, height }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 小草摇摆动画
  const sway = interpolate(
    Math.sin((frame + delay) * 0.1),
    [-1, 1],
    [-5, 5],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  return (
    <g transform={`translate(${x}, ${540 - height})`}>
      {/* 草叶 1 */}
      <path
        d={`M0,${height} Q${sway * 0.5},${height * 0.6} ${sway},${0}`}
        stroke="#4CAF50"
        strokeWidth="2"
        fill="none"
      />
      {/* 草叶 2 */}
      <path
        d={`M0,${height} Q${sway * 0.3},${height * 0.5} ${sway * 0.8},${-10}`}
        stroke="#66BB6A"
        strokeWidth="1.5"
        fill="none"
      />
      {/* 草叶 3 */}
      <path
        d={`M0,${height} Q${-sway * 0.4},${height * 0.7} ${-sway * 0.5},${-5}`}
        stroke="#43A047"
        strokeWidth="1.5"
        fill="none"
      />
    </g>
  );
};

// 小兔子组件
const Rabbit: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 兔子整体上下跳动（呼吸效果）
  const breatheY = interpolate(
    Math.sin(frame * 0.15),
    [-1, 1],
    [-2, 2],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  // 耳朵摆动
  const earSway = interpolate(
    Math.sin(frame * 0.2),
    [-1, 1],
    [-3, 3],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  // 咀嚼动作（嘴巴开合）
  const chewMouth = interpolate(
    Math.sin(frame * 0.4),
    [-1, 1],
    [0, 3],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  // 眨眼效果 - 每隔一段时间眨一次
  const blinkProgress = (frame % (fps * 3)) / (fps * 3);
  const eyeScaleY = blinkProgress < 0.1
    ? interpolate(blinkProgress, [0, 0.1], [0.1, 1])
    : 1;

  return (
    <g transform={`translate(540, ${320 + breatheY})`}>
      {/* 身体 - 白色毛绒绒 */}
      <ellipse cx="0" cy="80" rx="70" ry="50" fill="#F5F5F5" />
      <ellipse cx="-30" cy="75" rx="40" ry="35" fill="#FAFAFA" />

      {/* 尾巴 - 毛茸茸的小圆球 */}
      <circle cx="-65" cy="85" r="15" fill="#FAFAFA" />
      <circle cx="-70" cy="80" r="10" fill="#F0F0F0" />

      {/* 后腿 */}
      <ellipse cx="-40" cy="120" rx="25" ry="15" fill="#E8E8E8" />
      <ellipse cx="40" cy="120" rx="25" ry="15" fill="#E8E8E8" />

      {/* 前腿 - 正在吃草的姿势 */}
      <ellipse cx="-20" cy="115" rx="12" ry="20" fill="#F0F0F0" />
      <ellipse cx="20" cy="115" rx="12" ry="20" fill="#F0F0F0" />

      {/* 头部 */}
      <ellipse cx="0" cy="20" rx="45" ry="40" fill="#F5F5F5" />

      {/* 脸颊 - 粉粉嫩嫩的 */}
      <ellipse cx="-30" cy="30" rx="12" ry="8" fill="#FFB6C1" opacity="0.6" />
      <ellipse cx="30" cy="30" rx="12" ry="8" fill="#FFB6C1" opacity="0.6" />

      {/* 长耳朵 - 会摆动 */}
      <g transform={`rotate(${earSway * 0.5}, -15, -35)`}>
        <ellipse cx="-15" cy="-55" rx="10" ry="35" fill="#F5F5F5" />
        <ellipse cx="-15" cy="-55" rx="5" ry="25" fill="#FFB6C1" opacity="0.5" />
      </g>
      <g transform={`rotate(${earSway * 0.3}, 15, -35)`}>
        <ellipse cx="15" cy="-55" rx="10" ry="35" fill="#F5F5F5" />
        <ellipse cx="15" cy="-55" rx="5" ry="25" fill="#FFB6C1" opacity="0.5" />
      </g>

      {/* 眼睛 - 会眨 */}
      <g transform={`scale(1, ${eyeScaleY})`}>
        <ellipse cx="-20" cy="10" rx="6" ry="8" fill="#2C2C2C" />
        <ellipse cx="20" cy="10" rx="6" ry="8" fill="#2C2C2C" />
        {/* 眼睛高光 */}
        <circle cx="-18" cy="7" r="2.5" fill="white" />
        <circle cx="22" cy="7" r="2.5" fill="white" />
      </g>

      {/* 鼻子 - 粉色小三角 */}
      <polygon points="0,25 -5,32 5,32" fill="#FFB6C1" />

      {/* 嘴巴 - 咀嚼动作 */}
      <ellipse cx="0" cy={35 + chewMouth * 0.5} rx="8" ry={4 + chewMouth} fill="#FFB6C1" opacity="0.8" />

      {/* 胡须 */}
      <line x1="-10" y1="30" x2="-35" y2="25" stroke="#D0D0D0" strokeWidth="1" />
      <line x1="-10" y1="33" x2="-35" y2="33" stroke="#D0D0D0" strokeWidth="1" />
      <line x1="-10" y1="36" x2="-35" y2="41" stroke="#D0D0D0" strokeWidth="1" />
      <line x1="10" y1="30" x2="35" y2="25" stroke="#D0D0D0" strokeWidth="1" />
      <line x1="10" y1="33" x2="35" y2="33" stroke="#D0D0D0" strokeWidth="1" />
      <line x1="10" y1="36" x2="35" y2="41" stroke="#D0D0D0" strokeWidth="1" />

      {/* 前爪 - 拿着草 */}
      <ellipse cx="-15" cy="95" rx="10" ry="8" fill="#F0F0F0" />
      <ellipse cx="15" cy="95" rx="10" ry="8" fill="#F0F0F0" />

      {/* 嘴里的草 */}
      <line x1="-5" y1="40" x2="-15" y2="35" stroke="#4CAF50" strokeWidth="3" />
      <line x1="5" y1="40" x2="15" y2="35" stroke="#4CAF50" strokeWidth="3" />
    </g>
  );
};

// 主合成
export const RabbitComposition: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  // 淡入效果
  const opacity = interpolate(frame, [0, 30], [0, 1], {
    extrapolateRight: 'clamp',
  });

  // 生成小草的位置
  const grassPositions = Array.from({ length: 40 }, (_, i) => ({
    x: 50 + i * 28,
    delay: i * 5,
    height: 40 + Math.random() * 40,
  }));

  return (
    <div style={{
      width,
      height,
      backgroundColor: '#87CEEB',
      overflow: 'hidden',
      opacity
    }}>
      <svg width={width} height={height}>
        {/* 天空背景渐变 */}
        <defs>
          <linearGradient id="skyGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#4FC3F7" />
            <stop offset="100%" stopColor="#B3E5FC" />
          </linearGradient>
          <linearGradient id="grassGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#81C784" />
            <stop offset="100%" stopColor="#4CAF50" />
          </linearGradient>
          {/* 云朵渐变 */}
          <radialGradient id="cloudGradient">
            <stop offset="0%" stopColor="white" stopOpacity="1" />
            <stop offset="100%" stopColor="white" stopOpacity="0.8" />
          </radialGradient>
        </defs>

        {/* 天空 */}
        <rect width={width} height={height * 0.6} fill="url(#skyGradient)" />

        {/* 太阳 */}
        <circle cx="100" cy="80" r="50" fill="#FFD54F" opacity="0.9" />
        <circle cx="100" cy="80" r="40" fill="#FFCA28" />

        {/* 云朵 - 缓慢飘动 */}
        <g transform={`translate(${interpolate(frame % (fps * 20), [0, fps * 20], [0, 100])}, 0)`}>
          <ellipse cx="200" cy="60" rx="60" ry="30" fill="url(#cloudGradient)" />
          <ellipse cx="240" cy="50" rx="50" ry="35" fill="url(#cloudGradient)" />
          <ellipse cx="280" cy="60" rx="55" ry="28" fill="url(#cloudGradient)" />
        </g>
        <g transform={`translate(${interpolate((frame + 500) % (fps * 25), [0, fps * 25], [0, 80])}, 0)`}>
          <ellipse cx="600" cy="80" rx="50" ry="25" fill="url(#cloudGradient)" />
          <ellipse cx="640" cy="70" rx="45" ry="30" fill="url(#cloudGradient)" />
          <ellipse cx="680" cy="78" rx="48" ry="24" fill="url(#cloudGradient)" />
        </g>

        {/* 远山 */}
        <path
          d="M0,320 L150,200 L300,320 L450,180 L600,320 L750,220 L900,320 L1080,320 Z"
          fill="#90A4AE"
          opacity="0.6"
        />
        <path
          d="M0,320 L200,240 L400,320 L550,200 L700,320 L850,250 L1080,320 Z"
          fill="#78909C"
          opacity="0.5"
        />

        {/* 草地 */}
        <rect x="0" y="400" width={width} height={height - 400} fill="url(#grassGradient)" />

        {/* 小草 - 随风摇摆 */}
        {grassPositions.map((grass, index) => (
          <Grass
            key={index}
            x={grass.x}
            delay={grass.delay}
            height={grass.height}
          />
        ))}

        {/* 小兔子 */}
        <Rabbit />

        {/* 前景小草 - 增加层次感 */}
        {Array.from({ length: 20 }, (_, i) => (
          <Grass
            key={`fg-${i}`}
            x={30 + i * 55}
            delay={i * 3 + 100}
            height={30 + Math.random() * 20}
          />
        ))}

        {/* 小花点缀 */}
        <g transform="translate(100, 520)">
          <circle cx="0" cy="0" r="5" fill="#FF6B9D" />
          <circle cx="8" cy="0" r="5" fill="#FFB6C1" />
          <circle cx="-8" cy="0" r="5" fill="#FF69B4" />
          <circle cx="0" cy="8" r="5" fill="#FFB6C1" />
          <circle cx="0" cy="-8" r="5" fill="#FF6B9D" />
          <circle cx="0" cy="0" r="3" fill="#FFD700" />
        </g>
        <g transform="translate(950, 530)">
          <circle cx="0" cy="0" r="5" fill="#DDA0DD" />
          <circle cx="6" cy="0" r="5" fill="#EE82EE" />
          <circle cx="-6" cy="0" r="5" fill="#DDA0DD" />
          <circle cx="0" cy="6" r="5" fill="#EE82EE" />
          <circle cx="0" cy="-6" r="5" fill="#DDA0DD" />
          <circle cx="0" cy="0" r="3" fill="#FFD700" />
        </g>
      </svg>

      {/* 标题文字 */}
      <div style={{
        position: 'absolute',
        top: 20,
        left: 0,
        right: 0,
        textAlign: 'center',
        fontFamily: 'Georgia, serif',
        fontSize: 32,
        color: 'white',
        textShadow: '2px 2px 4px rgba(0,0,0,0.3)',
      }}>
        🐰 小兔子吃草 🌿
      </div>
    </div>
  );
};

export default RabbitComposition;
