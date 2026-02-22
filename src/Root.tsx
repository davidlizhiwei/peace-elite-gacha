import React from "react";
import { Composition } from "remotion";
import { RabbitComposition } from "./RabbitComposition";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/*
        1080p 分辨率，30fps，10 秒时长（300 帧）
        小兔子在草地上吃草的温馨场景
      */}
      <Composition
        id="Rabbit"
        component={RabbitComposition}
        durationInFrames={300}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{}}
      />
    </>
  );
};
