import { Composition } from "remotion";
import { SingleBlendVideo } from "./SingleBlendVideo";
import { AllBlendsVideo } from "./AllBlendsVideo";
import { blends } from "./blends";

// With bottle hero: 5s intro + 4s bottle + 4×3s ingredients + 6s text + 5s pricing - 7×1s transitions = 27s = 840 frames
const SINGLE_BLEND_FRAMES = 840;
// Combined: 5s intro + 4×(27s blend sections) + 4×1s transitions ≈ 117s
const ALL_BLENDS_FRAMES = 3500;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="SkinBoost"
        component={SingleBlendVideo}
        defaultProps={{ blend: blends.skinBoost }}
        durationInFrames={SINGLE_BLEND_FRAMES}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="Detox"
        component={SingleBlendVideo}
        defaultProps={{ blend: blends.detox }}
        durationInFrames={SINGLE_BLEND_FRAMES}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="ImmunityBoost"
        component={SingleBlendVideo}
        defaultProps={{ blend: blends.immunityBoost }}
        durationInFrames={SINGLE_BLEND_FRAMES}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="LiverKidney"
        component={SingleBlendVideo}
        defaultProps={{ blend: blends.liverKidney }}
        durationInFrames={SINGLE_BLEND_FRAMES}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="AllBlends"
        component={AllBlendsVideo}
        durationInFrames={ALL_BLENDS_FRAMES}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
