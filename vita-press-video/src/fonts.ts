import { loadFont as loadInstrumentSerif } from "@remotion/google-fonts/InstrumentSerif";
import { loadFont as loadDMSans } from "@remotion/google-fonts/DMSans";

export const { fontFamily: instrumentSerif } = loadInstrumentSerif("normal", {
  weights: ["400"],
  subsets: ["latin"],
});

export const { fontFamily: instrumentSerifItalic } = loadInstrumentSerif(
  "italic",
  {
    weights: ["400"],
    subsets: ["latin"],
  }
);

export const { fontFamily: dmSans } = loadDMSans("normal", {
  weights: ["300", "400", "500", "600"],
  subsets: ["latin"],
});
