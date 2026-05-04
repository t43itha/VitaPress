import { AbsoluteFill, useVideoConfig } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { IntroScene } from "./IntroScene";
import { IngredientClip } from "./IngredientClip";
import { JuiceTextCard } from "./JuiceTextCard";
import { theme } from "./theme";

export const VitaPressPromoV2: React.FC = () => {
  const { fps } = useVideoConfig();

  const TRANSITION_FRAMES = Math.round(1 * fps);
  const INTRO_DURATION = 5 * fps;
  const INGREDIENT_DURATION = 3 * fps; // slightly longer without bottle hero
  const TEXT_CARD_DURATION = 6 * fps;

  return (
    <AbsoluteFill style={{ backgroundColor: theme.bg }}>
      <TransitionSeries>
        {/* === INTRO === */}
        <TransitionSeries.Sequence durationInFrames={INTRO_DURATION}>
          <IntroScene />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
        />

        {/* === DETOX: Celery === */}
        <TransitionSeries.Sequence durationInFrames={INGREDIENT_DURATION}>
          <IngredientClip videoFile="celery.mp4" label="Celery" />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
        />

        {/* === DETOX: Lime === */}
        <TransitionSeries.Sequence durationInFrames={INGREDIENT_DURATION}>
          <IngredientClip videoFile="limes.mp4" label="Lime" />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
        />

        {/* === DETOX: Cucumber === */}
        <TransitionSeries.Sequence durationInFrames={INGREDIENT_DURATION}>
          <IngredientClip videoFile="cucumbers.mp4" label="Cucumber" />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
        />

        {/* === DETOX: Apple === */}
        <TransitionSeries.Sequence durationInFrames={INGREDIENT_DURATION}>
          <IngredientClip videoFile="apples.mp4" label="Apple" />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
        />

        {/* === DETOX: Text Card === */}
        <TransitionSeries.Sequence durationInFrames={TEXT_CARD_DURATION}>
          <JuiceTextCard
            name="Detox"
            ingredients="Celery · Lime · Cucumber · Apple"
            benefit="Hydration and gentle cleansing."
            accentColor={theme.juiceColors.detox}
            bottleImage="detox-bottle-transparent.png"
          />
        </TransitionSeries.Sequence>
      </TransitionSeries>
    </AbsoluteFill>
  );
};
