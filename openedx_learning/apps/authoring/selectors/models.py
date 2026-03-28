"""
Models that implement selectors
"""
from django.db import models

from ..publishing.mixins import PublishableEntityMixin, PublisahbleEntityVersionMixin
from ..publishing.models import EntityList, Container, ContainerVersion

__all__ = [
    "Selector",
    "SelectorVersion",
    "Variant",
]



class SelectionError(Exception):
    params: SelectionParams
    sv: SelectorVersion
    details: str

    def __str__(self):
        return f"could not determine variant for {self.sv} given {self.params}: {self.details}"



class Selector(PublishableEntityMixin):
    """
    A Selector is ...
    """


class SelectorVersion(PublishableEntityVersionMixin):
    """
    A SelectorVersion is ...
    """

    def select_new_variant(self, params: SelectionParams) -> Variant:
        """
        ...
        """
        raise NotImplementedError

    def update_variant(self, previously_selected: Variant, params: SelectionParams) -> Variant:
        """
        ...
        """
        raise NotImplementedError


class Variant(models.Model):
    """
    A Variant is...
    """
    selector_version = models.ForeignKey(SelectorVersion, on_delete=models.RESTRICT, related_name="variants")
    index = models.PositiveIntField(default=null, null=True)
    entity_list = models.ForiegnKey(EntityList, on_delete=models.RESTRICT)

    class Meta:
        unique_together = ("selector_version", "index")


### TODO: All SplitTest-related models should be moved into a separate splitests app.
###       Putting them here now for ease of discussion.


@dataclass(frozen=True)
class SplitTestSelectionParams(SelectionParams):
    group_id: int
    

class SplitTest(Selector):
    selector = models.ForiegnKey(
        Selector,
        on_delete=models.CASCADE,
        primary_key=True,
        parent_link=True,
    )

class SplitTestVersion(SelectorVersion):
    selector_version = models.ForiegnKey(
        SelectorVersion,
        on_delete=models.CASCADE,
        primary_key=True,
        parent_link=True,
    )

    def update_variant(self, previously_selected: Variant, params: SplitTestSelectionParams) -> Variant:
        if previously_selected.index == params.group_id:
            return Variant.objects.
        return self.select_new_variant(params)

    def select_new_variant(self, params: SplitTestSelectionParams) -> Variant:
        """
        ...
        """
        try:
            return self.selector_version.variants.get(index=params.group_id)
        except Variant.DoesNotExist as exc:
            raise SelectionError(sv=selector_version, params=params, details="No variant matching group_id")


### TODO: All ItemBank-related models should be moved into a separate itembanks app.
###       Putting them here now for ease of discussion.

class ItemBank(Selector):
    selector = models.ForiegnKey(
        Selector,
        on_delete=models.CASCADE,
        primary_key=True,
        parent_link=True,
    )

class ItemBankVersion(SelectorVersion):
    selector_version = models.ForiegnKey(
        SelectorVersion,
        on_delete=models.CASCADE,
        primary_key=True,
        parent_link=True,
    )
    pool = models.ForeignKey(EntityList, on_delete=models.RESTRICT)
    select_all = models.BooleanField(default=False)
    number_to_select = models.PositiveIntegerField(default=1)



