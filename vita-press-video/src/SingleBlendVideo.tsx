import { AbsoluteFill, useVideoConfig } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { IntroScene } from "./IntroScene";
import { buildBlendElements } from "./BlendSection";
import { theme } from "./theme";

interface BlendData {
  name: string;
  tagline: string;
  ingredients: { videoFile: string; label: string }[];
  ingredientsText: string;
  benefit: string;
  accentColor: string;
  bottleImage: string;
}

export const SingleBlendVideo: React.FC<{ blend: BlendData }> = ({ blend }) => {
  const { fps } = useVideoConfig();
  const TRANSITION = Math.round(1 * fps);
  const INTRO_DURATION = 5 * fps;

  return (
    <AbsoluteFill style={{ backgroundColor: theme.bg }}>
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={INTRO_DURATION}>
          <IntroScene />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION })}
        />

        {buildBlendElements(blend, fps, blend.name)}
      </TransitionSeries>
    </AbsoluteFill>
  );
};
