import { AbsoluteFill, useVideoConfig } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { IntroScene } from "./IntroScene";
import { buildBlendElements } from "./BlendSection";
import { blends } from "./blends";
import { theme } from "./theme";

export const AllBlendsVideo: React.FC = () => {
  const { fps } = useVideoConfig();
  const TRANSITION = Math.round(1 * fps);
  const INTRO_DURATION = 5 * fps;

  const blendOrder = [blends.skinBoost, blends.detox, blends.immunityBoost, blends.liverKidney];

  return (
    <AbsoluteFill style={{ backgroundColor: theme.bg }}>
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={INTRO_DURATION}>
          <IntroScene />
        </TransitionSeries.Sequence>

        {blendOrder.flatMap((blend) => [
          <TransitionSeries.Transition
            key={`${blend.name}-intro-trans`}
            presentation={fade()}
            timing={linearTiming({ durationInFrames: TRANSITION })}
          />,
          ...buildBlendElements(blend, fps, blend.name),
        ])}
      </TransitionSeries>
    </AbsoluteFill>
  );
};
