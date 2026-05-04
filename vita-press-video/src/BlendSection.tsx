import React from "react";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { BottleHero } from "./BottleHero";
import { IngredientClip } from "./IngredientClip";
import { JuiceTextCard } from "./JuiceTextCard";
import { PricingSlide } from "./PricingSlide";

interface Ingredient {
  videoFile: string;
  label: string;
}

interface BlendConfig {
  name: string;
  ingredients: Ingredient[];
  ingredientsText: string;
  benefit: string;
  accentColor: string;
  bottleImage: string;
  tagline: string;
  bottleVideo?: string;
  bottleVideoTrim?: number;
}

export function buildBlendElements(
  blend: BlendConfig,
  fps: number,
  prefix: string
): React.ReactNode[] {
  const TRANSITION = Math.round(1 * fps);
  const BOTTLE_HERO_DURATION = 4 * fps;
  const INGREDIENT_DURATION = 3 * fps;
  const TEXT_CARD_DURATION = 6 * fps;
  const PRICING_DURATION = 5 * fps;

  const elements: React.ReactNode[] = [];

  // Bottle hero (if video available)
  if (blend.bottleVideo) {
    elements.push(
      <TransitionSeries.Sequence
        key={`${prefix}-bottle`}
        durationInFrames={BOTTLE_HERO_DURATION}
      >
        <BottleHero
          videoFile={blend.bottleVideo}
          trimStartSeconds={blend.bottleVideoTrim ?? 0}
        />
      </TransitionSeries.Sequence>
    );
    elements.push(
      <TransitionSeries.Transition
        key={`${prefix}-bottle-trans`}
        presentation={fade()}
        timing={linearTiming({ durationInFrames: TRANSITION })}
      />
    );
  }

  // Ingredient clips
  blend.ingredients.forEach((ing, i) => {
    if (i > 0 || blend.bottleVideo) {
      // Add transition before ingredient (skip first if no bottle hero)
      if (i > 0) {
        elements.push(
          <TransitionSeries.Transition
            key={`${prefix}-ing-trans-${i}`}
            presentation={fade()}
            timing={linearTiming({ durationInFrames: TRANSITION })}
          />
        );
      }
    }
    elements.push(
      <TransitionSeries.Sequence
        key={`${prefix}-ing-${i}`}
        durationInFrames={INGREDIENT_DURATION}
      >
        <IngredientClip videoFile={ing.videoFile} label={ing.label} />
      </TransitionSeries.Sequence>
    );
  });

  // Transition to text card
  elements.push(
    <TransitionSeries.Transition
      key={`${prefix}-text-trans`}
      presentation={fade()}
      timing={linearTiming({ durationInFrames: TRANSITION })}
    />
  );

  // Text card
  elements.push(
    <TransitionSeries.Sequence
      key={`${prefix}-text`}
      durationInFrames={TEXT_CARD_DURATION}
    >
      <JuiceTextCard
        name={blend.name}
        tagline={blend.tagline}
        ingredients={blend.ingredientsText}
        benefit={blend.benefit}
        accentColor={blend.accentColor}
        bottleImage={blend.bottleImage}
      />
    </TransitionSeries.Sequence>
  );

  // Transition to pricing
  elements.push(
    <TransitionSeries.Transition
      key={`${prefix}-price-trans`}
      presentation={fade()}
      timing={linearTiming({ durationInFrames: TRANSITION })}
    />
  );

  // Pricing slide
  elements.push(
    <TransitionSeries.Sequence
      key={`${prefix}-price`}
      durationInFrames={PRICING_DURATION}
    >
      <PricingSlide />
    </TransitionSeries.Sequence>
  );

  return elements;
}
