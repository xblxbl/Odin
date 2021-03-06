import pandas as pd
from odin.strategy import AbstractStrategy
from odin.strategy.templates import BuyAndHoldStrategy
from odin.utilities.mixins.strategy_mixins import (
    LongStrategyMixin,
    TotalSellProportionMixin,
    AlwaysBuyIndicatorMixin,
    NeverSellIndicatorMixin,
    DefaultPriorityMixin,
    DefaultFeaturesMixin,
)


class BuyAndHoldSpyderStrategy(BuyAndHoldStrategy):
    def buy_indicator(self, feats):
        return feats.name in ("SPY", )


class RebalanceETFStrategy(
    LongStrategyMixin,
    TotalSellProportionMixin,
    AlwaysBuyIndicatorMixin,
    NeverSellIndicatorMixin,
    DefaultPriorityMixin,
    DefaultFeaturesMixin,
):
    def compute_buy_proportion(self, feats):
        """Implementation of abstract base class method."""
        if feats.name == "SPY":
            return 0.6
        elif feats.name == "AGG":
            return 0.4
    
    def exit_indicator(self, feats):
        """Implementation of abstract base class method."""
        symbol = feats.name
        pos = self.portfolio.portfolio_handler.filled_positions[symbol]
        date = self.portfolio.data_handler.current_date
        return pos.compute_holding_period(date).days > 63
